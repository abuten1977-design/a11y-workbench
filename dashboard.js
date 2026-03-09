        let currentProjectId = null;
        let currentTargetId = null;
        let activeSessionId = null;
        let currentIssueId = null;
        let wcagCriteria = [];
        
        // Load WCAG criteria on startup
        async function loadWCAG() {
            try {
                const wcagFile = await fetch('/wcag_criteria_simple.json');
                wcagCriteria = await wcagFile.json();
            } catch (err) {
                console.error('Failed to load WCAG:', err);
            }
        }
        
        // Load projects
        async function loadProjects() {
            const res = await fetch('/api/v1/projects');
            const data = await res.json();
            
            const list = document.getElementById('projects-list');
            if (data.projects.length === 0) {
                list.innerHTML = '<div class="empty">No projects yet. Create one!</div>';
            } else {
                list.innerHTML = data.projects.map(p => `
                    <div class="list-item">
                        <div>
                            <div class="list-item-title">${p.name}</div>
                            <div class="list-item-meta">${p.client_name || 'No client'} • ${p.status}</div>
                        </div>
                        <div style="display: flex; gap: 8px;">
                            <button class="btn-primary" onclick="selectProject('${p.id}')">Open</button>
                            <button class="btn-secondary" onclick="showExportMenu('${p.id}')">📥 Export</button>
                        </div>
                    </div>
                `).join('');
            }
        }
        
        // Show export menu
        function showExportMenu(projectId) {
            const menu = `
                <div style="margin-top: 10px; padding: 10px; background: #2a2a2a; border-radius: 6px;">
                    <strong>Export Options:</strong>
                    <div style="margin-top: 10px; display: flex; gap: 8px; flex-wrap: wrap;">
                        <a href="/api/v1/projects/${projectId}/export/markdown" download="report.md" class="btn-primary" style="text-decoration: none;">📄 Markdown</a>
                        <a href="/api/v1/projects/${projectId}/export/json" download="report.json" class="btn-primary" style="text-decoration: none;">📊 JSON</a>
                        <a href="/api/v1/projects/${projectId}/export/csv" download="report.csv" class="btn-primary" style="text-decoration: none;">📋 CSV</a>
                        <button class="btn-secondary" onclick="showStatistics('${projectId}')">📈 Stats</button>
                    </div>
                </div>
            `;
            
            // Find the project item and add menu
            const projectItems = document.querySelectorAll('.list-item');
            projectItems.forEach(item => {
                const existingMenu = item.querySelector('.export-menu');
                if (existingMenu) existingMenu.remove();
            });
            
            const projectItem = event.target.closest('.list-item');
            const menuDiv = document.createElement('div');
            menuDiv.className = 'export-menu';
            menuDiv.innerHTML = menu;
            projectItem.appendChild(menuDiv);
        }
        
        // Show statistics
        async function showStatistics(projectId) {
            const res = await fetch(`/api/v1/projects/${projectId}/statistics`);
            const stats = await res.json();
            
            const content = `
                <h3>📈 Project Statistics</h3>
                <div style="margin-top: 15px;">
                    <p><strong>Total Issues:</strong> ${stats.total_issues}</p>
                    <p><strong>By Severity:</strong></p>
                    <ul>
                        <li>Critical: ${stats.by_severity.critical || 0}</li>
                        <li>Serious: ${stats.by_severity.serious || 0}</li>
                        <li>Moderate: ${stats.by_severity.moderate || 0}</li>
                        <li>Minor: ${stats.by_severity.minor || 0}</li>
                    </ul>
                    <p><strong>WCAG Criteria:</strong> ${stats.wcag_criteria.join(', ') || 'None'}</p>
                </div>
            `;
            
            showModal('Statistics', content);
        }
        
        // Select project
        async function selectProject(projectId) {
            currentProjectId = projectId;
            document.getElementById('targets-section').classList.remove('hidden');
            document.getElementById('sessions-section').classList.remove('hidden');
            document.getElementById('groups-section').classList.remove('hidden');
            document.getElementById('issues-section').classList.remove('hidden');
            loadTargets();
            loadSessions();
            loadGroups();
            loadIssues();
        }
        
        // Load targets
        async function loadTargets() {
            if (!currentProjectId) return;
            
            const res = await fetch(`/api/v1/projects/${currentProjectId}/targets`);
            const data = await res.json();
            
            const list = document.getElementById('targets-list');
            if (data.targets.length === 0) {
                list.innerHTML = '<div class="empty">No targets yet. Add one!</div>';
            } else {
                list.innerHTML = data.targets.map(t => `
                    <div class="list-item">
                        <div>
                            <div class="list-item-title">${t.name}</div>
                            <div class="list-item-meta">${t.url} • ${t.flow_type}</div>
                        </div>
                        <button class="btn-primary" onclick="selectTarget('${t.id}')">Select</button>
                    </div>
                `).join('');
            }
        }
        
        // Select target
        function selectTarget(targetId) {
            currentTargetId = targetId;
            alert('Target selected! Now issues will be linked to this target.');
        }
        
        // Load sessions
        async function loadSessions() {
            if (!currentProjectId) return;
            
            const res = await fetch(`/api/v1/projects/${currentProjectId}/sessions`);
            const data = await res.json();
            
            const list = document.getElementById('sessions-list');
            if (data.sessions.length === 0) {
                list.innerHTML = '<div class="empty">No sessions yet. Start one!</div>';
            } else {
                list.innerHTML = data.sessions.map(s => {
                    const status = s.completed_at ? '✅ Completed' : '🟢 Active';
                    const duration = s.completed_at ? 
                        `${Math.round((new Date(s.completed_at) - new Date(s.started_at)) / 60000)} min` : 
                        'In progress';
                    return `
                        <div class="list-item">
                            <div>
                                <div class="list-item-title">${s.assistive_tech} + ${s.browser}</div>
                                <div class="list-item-meta">${status} • ${duration} • ${s.platform}</div>
                            </div>
                        </div>
                    `;
                }).join('');
            }
            
            // Check for active session
            const active = data.sessions.find(s => !s.completed_at);
            if (active) {
                activeSessionId = active.id;
                document.getElementById('active-session').classList.remove('hidden');
                document.getElementById('active-session-info').textContent = 
                    `${active.assistive_tech} + ${active.browser} on ${active.platform}`;
            } else {
                activeSessionId = null;
                document.getElementById('active-session').classList.add('hidden');
            }
        }
        
        // Load groups
        async function loadGroups() {
            if (!currentProjectId) return;
            
            const res = await fetch(`/api/v1/projects/${currentProjectId}/groups`);
            const data = await res.json();
            
            const list = document.getElementById('groups-list');
            if (data.groups.length === 0) {
                list.innerHTML = '<div class="empty">No groups yet. Create one!</div>';
            } else {
                list.innerHTML = data.groups.map(g => `
                    <div class="list-item">
                        <div>
                            <div class="list-item-title">${g.name}</div>
                            <div class="list-item-meta">${g.category}</div>
                        </div>
                    </div>
                `).join('');
            }
        }
        
        // Load issues
        async function loadIssues() {
            if (!currentProjectId) return;
            
            // Build query params
            const params = new URLSearchParams();
            const severity = document.getElementById('filter-severity')?.value;
            const status = document.getElementById('filter-status')?.value;
            
            if (severity) params.append('severity', severity);
            if (status) params.append('status', status);
            
            const res = await fetch(`/api/v1/projects/${currentProjectId}/issues?${params}`);
            const data = await res.json();
            
            // Client-side search filter
            const searchTerm = document.getElementById('filter-search')?.value.toLowerCase() || '';
            let filtered = data.issues;
            if (searchTerm) {
                filtered = filtered.filter(i => 
                    i.title.toLowerCase().includes(searchTerm) ||
                    (i.description && i.description.toLowerCase().includes(searchTerm))
                );
            }
            
            const list = document.getElementById('issues-list');
            if (filtered.length === 0) {
                list.innerHTML = '<div class="empty">No issues found</div>';
            } else {
                list.innerHTML = filtered.map(i => `
                    <div class="list-item">
                        <div>
                            <div class="list-item-title">${i.title}</div>
                            <div class="list-item-meta">
                                <span class="badge badge-${i.severity}">${i.severity}</span>
                                ${i.status ? `<span style="opacity: 0.7;">• ${i.status}</span>` : ''}
                                ${i.wcag_criterion ? `<span style="opacity: 0.7;">• ${i.wcag_criterion}</span>` : ''}
                            </div>
                        </div>
                        <button class="btn-primary" onclick="viewIssue('${i.id}')">View</button>
                    </div>
                `).join('');
            }
        }
        
        // Clear filters
        function clearFilters() {
            document.getElementById('filter-search').value = '';
            document.getElementById('filter-severity').value = '';
            document.getElementById('filter-status').value = '';
            loadIssues();
        }
        
        // Show/hide forms
        function showCreateProject() {
            document.getElementById('create-project-form').classList.remove('hidden');
        }
        function hideCreateProject() {
            document.getElementById('create-project-form').classList.add('hidden');
        }
        function showCreateTarget() {
            if (!currentProjectId) {
                alert('Select a project first!');
                return;
            }
            document.getElementById('create-target-form').classList.remove('hidden');
        }
        function hideCreateTarget() {
            document.getElementById('create-target-form').classList.add('hidden');
        }
        async function showStartSession() {
            if (!currentProjectId) {
                alert('Select a project first!');
                return;
            }
            if (activeSessionId) {
                alert('End current session first!');
                return;
            }
            
            // Load targets into dropdown
            const res = await fetch(`/api/v1/projects/${currentProjectId}/targets`);
            const data = await res.json();
            const select = document.getElementById('session-target-id');
            select.innerHTML = '<option value="">Select target...</option>' + 
                data.targets.map(t => `<option value="${t.id}">${t.name}</option>`).join('');
            
            document.getElementById('start-session-form').classList.remove('hidden');
        }
        function hideStartSession() {
            document.getElementById('start-session-form').classList.add('hidden');
        }
        function showCreateGroup() {
            if (!currentProjectId) {
                alert('Select a project first!');
                return;
            }
            document.getElementById('create-group-form').classList.remove('hidden');
        }
        function hideCreateGroup() {
            document.getElementById('create-group-form').classList.add('hidden');
        }
        async function showCreateIssue() {
            if (!currentProjectId) {
                alert('Select a project first!');
                return;
            }
            
            // Load groups into dropdown
            const res = await fetch(`/api/v1/projects/${currentProjectId}/groups`);
            const data = await res.json();
            const select = document.getElementById('issue-group-id');
            select.innerHTML = '<option value="">No group</option>' + 
                data.groups.map(g => `<option value="${g.id}">${g.name}</option>`).join('');
            
            document.getElementById('create-issue-form').classList.remove('hidden');
        }
        function hideCreateIssue() {
            document.getElementById('create-issue-form').classList.add('hidden');
        }
        async function showDetailedIssue() {
            if (!currentProjectId) {
                alert('Select a project first!');
                return;
            }
            
            // Load groups into dropdown
            const res = await fetch(`/api/v1/projects/${currentProjectId}/groups`);
            const data = await res.json();
            const select = document.getElementById('detailed-group-id');
            select.innerHTML = '<option value="">No group</option>' + 
                data.groups.map(g => `<option value="${g.id}">${g.name}</option>`).join('');
            
            // Load WCAG into dropdown
            const wcagSelect = document.getElementById('detailed-wcag');
            wcagSelect.innerHTML = '<option value="">Select WCAG...</option>' + 
                wcagCriteria.map(c => `<option value="${c.id}">${c.id} - ${c.title}</option>`).join('');
            
            document.getElementById('detailed-issue-form').classList.remove('hidden');
        }
        function hideDetailedIssue() {
            document.getElementById('detailed-issue-form').classList.add('hidden');
        }
        
        // Create project
        async function createProject() {
            const name = document.getElementById('project-name').value;
            if (!name) {
                alert('Project name required!');
                return;
            }
            
            const data = {
                name,
                client_name: document.getElementById('project-client').value || null,
                description: document.getElementById('project-description').value || null
            };
            
            const res = await fetch('/api/v1/projects', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                hideCreateProject();
                document.getElementById('project-name').value = '';
                document.getElementById('project-client').value = '';
                document.getElementById('project-description').value = '';
                loadProjects();
                loadGlobalStats(); // Update stats
            }
        }
        
        // Create target
        async function createTarget() {
            const name = document.getElementById('target-name').value;
            const url = document.getElementById('target-url').value;
            
            if (!name || !url) {
                alert('Name and URL required!');
                return;
            }
            
            const data = {
                project_id: currentProjectId,
                name,
                url,
                flow_type: document.getElementById('target-flow-type').value,
                notes: document.getElementById('target-notes').value || null
            };
            
            const res = await fetch('/api/v1/targets', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                hideCreateTarget();
                document.getElementById('target-name').value = '';
                document.getElementById('target-url').value = '';
                document.getElementById('target-notes').value = '';
                loadTargets();
            }
        }
        
        // Start session
        async function startSession() {
            try {
                const targetId = document.getElementById('session-target-id').value;
                const at = document.getElementById('session-at').value;
                const browser = document.getElementById('session-browser').value;
                const platform = document.getElementById('session-platform').value;
                
                if (!targetId) {
                    alert('Select a target!');
                    return;
                }
                
                if (!currentProjectId) {
                    alert('No project selected!');
                    return;
                }
                
                const data = {
                    project_id: currentProjectId,
                    target_id: targetId,
                    assistive_tech: at,
                    browser: browser,
                    platform: platform,
                    tester_notes: document.getElementById('session-notes').value || null
                };
                
                console.log('Creating session:', data);
                
                const res = await fetch('/api/v1/sessions', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                if (res.ok) {
                    hideStartSession();
                    document.getElementById('session-notes').value = '';
                    await loadSessions();
                    alert('Session started!');
                } else {
                    const error = await res.text();
                    alert('Error: ' + error);
                }
            } catch (err) {
                console.error('Error starting session:', err);
                alert('Error: ' + err.message);
            }
        }
        
        // End session
        async function endSession() {
            if (!activeSessionId) {
                alert('No active session found. Please refresh the page.');
                console.error('activeSessionId is null');
                return;
            }
            
            try {
                console.log('Ending session:', activeSessionId);
                const res = await fetch(`/api/v1/sessions/${activeSessionId}/end`, {
                    method: 'PUT'
                });
                
                if (res.ok) {
                    activeSessionId = null;
                    await loadSessions();
                    alert('Session ended successfully!');
                } else {
                    const error = await res.text();
                    alert('Error ending session: ' + error);
                }
            } catch (err) {
                console.error('Error ending session:', err);
                alert('Error: ' + err.message);
            }
        }
        
        // Create group
        async function createGroup() {
            const name = document.getElementById('group-name').value;
            if (!name) {
                alert('Group name required!');
                return;
            }
            
            const data = {
                project_id: currentProjectId,
                target_id: currentTargetId,
                name,
                category: document.getElementById('group-category').value,
                notes: document.getElementById('group-notes').value || null
            };
            
            const res = await fetch('/api/v1/groups', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                hideCreateGroup();
                document.getElementById('group-name').value = '';
                document.getElementById('group-notes').value = '';
                loadGroups();
            }
        }
        
        // AI Expand Note
        async function aiExpandNote() {
            const rawNote = document.getElementById('issue-note').value;
            let htmlCode = document.getElementById('issue-html').value;
            const autoFetch = document.getElementById('auto-fetch-html').checked;
            
            if (!rawNote) {
                alert('Please enter a note first!');
                return;
            }
            
            // Auto-fetch HTML if checkbox is checked and no HTML provided
            if (autoFetch && !htmlCode && currentTargetId) {
                try {
                    htmlCode = await fetchTargetHTML();
                } catch (e) {
                    console.error('Failed to fetch HTML:', e);
                }
            }
            
            // Show loading
            const btn = event.target;
            const originalText = btn.textContent;
            btn.textContent = '⏳ AI thinking...';
            btn.disabled = true;
            
            try {
                const res = await fetch('/api/v1/ai/expand', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        raw_note: rawNote,
                        html_code: htmlCode || null,
                        project_id: currentProjectId,
                        target_url: currentTargetId
                    })
                });
                
                const data = await res.json();
                
                if (data.success) {
                    // Fill form with AI results
                    const result = data.result;
                    
                    document.getElementById('issue-title').value = result.title;
                    document.getElementById('issue-severity').value = result.severity;
                    
                    // Show detailed form with full data
                    showDetailedIssue();
                    
                    document.getElementById('detailed-title').value = result.title;
                    document.getElementById('detailed-steps').value = result.steps.join('\\n');
                    document.getElementById('detailed-observed').value = result.observed;
                    document.getElementById('detailed-expected').value = result.expected;
                    document.getElementById('detailed-impact').value = result.impact;
                    document.getElementById('detailed-severity').value = result.severity;
                    
                    // Add WCAG criteria (try to select first one in dropdown)
                    if (result.wcag && result.wcag.length > 0) {
                        const firstWcag = result.wcag[0].id;
                        const wcagSelect = document.getElementById('detailed-wcag');
                        
                        // Try to find and select the WCAG in dropdown
                        for (let option of wcagSelect.options) {
                            if (option.value.includes(firstWcag)) {
                                wcagSelect.value = option.value;
                                break;
                            }
                        }
                        
                        // If multiple WCAG, add to notes
                        if (result.wcag.length > 1) {
                            const allWcag = result.wcag.map(w => `${w.id} ${w.name} (${Math.round(w.confidence * 100)}%)`).join('\\n');
                            document.getElementById('detailed-notes').value = `Additional WCAG:\\n${allWcag}\\n\\n`;
                        }
                    }
                    
                    // Add fix to Suggested Fix field
                    if (result.fix) {
                        document.getElementById('detailed-fix').value = result.fix;
                    }
                    
                    alert(`✅ AI generated report!\nProcessing time: ${data.processing_time}s\n\nWCAG: ${result.wcag.map(w => w.id).join(', ')}\n\nPlease review and edit before saving.`);
                } else {
                    alert('AI error: ' + (data.error || 'Unknown error'));
                }
            } catch (e) {
                alert('Failed to call AI: ' + e.message);
            } finally {
                btn.textContent = originalText;
                btn.disabled = false;
            }
        }
        
        // Create issue
        async function createIssue() {
            const title = document.getElementById('issue-title').value;
            if (!title) {
                alert('Title required!');
                return;
            }
            
            const data = {
                project_id: currentProjectId,
                target_id: currentTargetId,
                finding_group_id: document.getElementById('issue-group-id').value || null,
                title,
                raw_note: document.getElementById('issue-note').value || null,
                severity: document.getElementById('issue-severity').value
            };
            
            const res = await fetch('/api/v1/issues', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                hideCreateIssue();
                document.getElementById('issue-title').value = '';
                document.getElementById('issue-note').value = '';
                loadIssues();
                loadGlobalStats(); // Update stats
            }
        }
        
        // Create detailed issue
        async function createDetailedIssue() {
            const title = document.getElementById('detailed-title').value;
            if (!title) {
                alert('Title required!');
                return;
            }
            
            const data = {
                project_id: currentProjectId,
                target_id: currentTargetId,
                session_id: activeSessionId,
                finding_group_id: document.getElementById('detailed-group-id').value || null,
                title,
                steps_to_reproduce: document.getElementById('detailed-steps').value || null,
                observed_behavior: document.getElementById('detailed-observed').value || null,
                expected_behavior: document.getElementById('detailed-expected').value || null,
                user_impact: document.getElementById('detailed-impact').value || null,
                affected_element: document.getElementById('detailed-element').value || null,
                wcag_criterion: document.getElementById('detailed-wcag').value || null,
                suggested_fix: document.getElementById('detailed-fix').value || null,
                severity: document.getElementById('detailed-severity').value,
                confidence: document.getElementById('detailed-confidence').value,
                source_type: 'manual',
                status: 'new'
            };
            
            const res = await fetch('/api/v1/issues', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                hideDetailedIssue();
                // Clear form
                document.getElementById('detailed-title').value = '';
                document.getElementById('detailed-steps').value = '';
                document.getElementById('detailed-observed').value = '';
                document.getElementById('detailed-expected').value = '';
                document.getElementById('detailed-impact').value = '';
                document.getElementById('detailed-element').value = '';
                document.getElementById('detailed-fix').value = '';
                loadIssues();
                loadGlobalStats(); // Update stats
            }
        }
        
        // View issue detail
        async function viewIssue(issueId) {
            currentIssueId = issueId;
            
            const res = await fetch(`/api/v1/issues/${issueId}`);
            const issue = await res.json();
            
            document.getElementById('modal-title').textContent = issue.title;
            
            let content = `
                <div style="display: grid; gap: 15px;">
                    ${issue.severity ? `<div><strong>Severity:</strong> <span class="badge badge-${issue.severity}">${issue.severity}</span></div>` : ''}
                    ${issue.wcag_criterion ? `<div><strong>WCAG:</strong> ${issue.wcag_criterion}</div>` : ''}
                    ${issue.affected_element ? `<div><strong>Element:</strong> <code>${issue.affected_element}</code></div>` : ''}
                    ${issue.steps_to_reproduce ? `<div><strong>Steps:</strong><pre style="background: #1a1a1a; padding: 10px; border-radius: 4px; white-space: pre-wrap;">${issue.steps_to_reproduce}</pre></div>` : ''}
                    ${issue.observed_behavior ? `<div><strong>Observed:</strong> ${issue.observed_behavior}</div>` : ''}
                    ${issue.expected_behavior ? `<div><strong>Expected:</strong> ${issue.expected_behavior}</div>` : ''}
                    ${issue.user_impact ? `<div><strong>Impact:</strong> ${issue.user_impact}</div>` : ''}
                    ${issue.suggested_fix ? `<div><strong>Fix:</strong> ${issue.suggested_fix}</div>` : ''}
                    ${issue.raw_note ? `<div><strong>Note:</strong> ${issue.raw_note}</div>` : ''}
                </div>
            `;
            
            document.getElementById('modal-content').innerHTML = content;
            
            // Load evidence
            const evidenceRes = await fetch(`/api/v1/issues/${issueId}/evidence`);
            const evidenceData = await evidenceRes.json();
            
            const evidenceList = document.getElementById('evidence-list');
            if (evidenceData.evidence.length === 0) {
                evidenceList.innerHTML = '<div class="empty">No evidence yet</div>';
            } else {
                evidenceList.innerHTML = evidenceData.evidence.map(e => `
                    <div style="background: #1a1a1a; padding: 15px; border-radius: 6px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <strong>${e.type.replace('_', ' ')}</strong>
                            <span style="opacity: 0.6; font-size: 12px;">${new Date(e.created_at).toLocaleString()}</span>
                        </div>
                        <pre style="white-space: pre-wrap; margin: 0;">${e.content}</pre>
                    </div>
                `).join('');
            }
            
            document.getElementById('issue-modal').classList.remove('hidden');
        }
        
        function closeIssueModal() {
            document.getElementById('issue-modal').classList.add('hidden');
            currentIssueId = null;
            document.getElementById('evidence-content').value = '';
        }
        
        function updateEvidenceLabel() {
            const type = document.getElementById('evidence-type').value;
            const label = document.getElementById('evidence-content-label');
            const labels = {
                'screen_reader_output': 'Screen Reader Output',
                'code': 'Code Snippet',
                'aria_dump': 'ARIA Info',
                'note': 'Notes'
            };
            label.textContent = labels[type] || 'Content';
        }
        
        async function addEvidence() {
            if (!currentIssueId) return;
            
            const content = document.getElementById('evidence-content').value;
            if (!content) {
                alert('Content required!');
                return;
            }
            
            const data = {
                issue_id: currentIssueId,
                type: document.getElementById('evidence-type').value,
                content: content
            };
            
            const res = await fetch('/api/v1/evidence', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                document.getElementById('evidence-content').value = '';
                viewIssue(currentIssueId); // Reload
            }
        }
        
        // Search debounce
        let searchTimeout;
        document.addEventListener('DOMContentLoaded', () => {
            const searchInput = document.getElementById('filter-search');
            if (searchInput) {
                searchInput.addEventListener('input', () => {
                    clearTimeout(searchTimeout);
                    searchTimeout = setTimeout(() => loadIssues(), 300);
                });
            }
            
            // Load global statistics
            loadGlobalStats();
        });
        
        // Load global statistics
        async function loadGlobalStats() {
            try {
                const res = await fetch('/api/v1/statistics');
                const stats = await res.json();
                
                const statsBar = document.getElementById('global-stats');
                statsBar.innerHTML = `
                    <div class="stat-item">
                        <div class="stat-value">${stats.total_projects || 0}</div>
                        <div class="stat-label">Projects</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${stats.total_issues || 0}</div>
                        <div class="stat-label">Total Issues</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${stats.by_severity?.critical || 0}</div>
                        <div class="stat-label">Critical</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${stats.by_severity?.serious || 0}</div>
                        <div class="stat-label">Serious</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${stats.wcag_criteria?.length || 0}</div>
                        <div class="stat-label">WCAG Criteria</div>
                    </div>
                `;
            } catch (err) {
                console.error('Failed to load stats:', err);
            }
        }
        
        // Load on start
        loadWCAG();
        loadProjects();

        // Fetch HTML from target URL
        async function fetchTargetHTML() {
            if (!currentTargetId) {
                alert('Please select a target first!');
                return '';
            }
            
            // Get target URL
            const targets = await fetch(`/api/v1/projects/${currentProjectId}/targets`).then(r => r.json());
            const target = targets.targets.find(t => t.id === currentTargetId);
            
            if (!target || !target.url) {
                alert('Target has no URL!');
                return '';
            }
            
            try {
                // Fetch HTML through proxy to avoid CORS
                const response = await fetch(`/api/v1/proxy?url=${encodeURIComponent(target.url)}`);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                const html = await response.text();
                return html;
            } catch (e) {
                alert(`Failed to fetch HTML from ${target.url}: ${e.message}`);
                return '';
            }
        }
        
        // Fetch and fill HTML field
        async function fetchPageHTML() {
            const btn = event.target;
            const originalText = btn.textContent;
            btn.textContent = '⏳ Fetching...';
            btn.disabled = true;
            
            try {
                const html = await fetchTargetHTML();
                if (html) {
                    document.getElementById('issue-html').value = html;
                    alert(`✅ Fetched ${html.length} characters of HTML`);
                }
            } catch (e) {
                alert('Error: ' + e.message);
            } finally {
                btn.textContent = originalText;
                btn.disabled = false;
            }
        }
