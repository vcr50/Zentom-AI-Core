Boolean hasSentinelFlow = false;
for (Schema.PicklistEntry entry : Case.Origin.getDescribe().getPicklistValues()) {
    if (entry.isActive() && entry.getValue() == 'SentinelFlow') {
        hasSentinelFlow = true;
    }
}
System.debug('Case Origin SentinelFlow active: ' + hasSentinelFlow);
