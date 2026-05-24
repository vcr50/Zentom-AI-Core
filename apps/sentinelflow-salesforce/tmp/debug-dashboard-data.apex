ZentomDashboardController.DashboardData data =
    ZentomDashboardController.getDashboardData('ALL');

System.debug('Total Incidents: ' + data.summary.totalIncidents);
System.debug('Critical Incidents: ' + data.summary.criticalIncidents);
System.debug('Pending Approvals: ' + data.summary.pendingApprovals);
System.debug('Executed Actions: ' + data.summary.executedActions);
System.debug('Approval Required: ' + data.summary.approvalRequired);
System.debug('Top Runbook: ' + data.summary.topRunbook);
System.debug('Recent Incidents: ' + data.recentIncidents.size());
System.debug('Pending Approval Rows: ' + data.pendingApprovals.size());
System.debug('Recent Executions: ' + data.recentExecutions.size());
