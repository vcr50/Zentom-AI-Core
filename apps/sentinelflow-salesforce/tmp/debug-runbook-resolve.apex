ZentomRunbookService.RunbookResult runbook =
    ZentomRunbookService.resolve('FLOW_FAILURE_BASIC_RECOVERY', 'FLOW_FAILURE');

System.debug('Runbook is null? ' + (runbook == null));
if (runbook != null) {
    System.debug('Runbook key: ' + runbook.runbookKey);
    System.debug('Runbook title: ' + runbook.title);
    System.debug('Runbook steps: ' + runbook.steps);
}
