CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    salesforce_org_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    tenant_id INT REFERENCES tenants(id),
    source VARCHAR(100),
    incident_type VARCHAR(100),
    severity VARCHAR(50),
    status VARCHAR(50),
    raw_payload JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    incident_id INT REFERENCES incidents(id),
    summary TEXT,
    root_cause TEXT,
    recommended_action TEXT,
    confidence_score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE risk_scores (
    id SERIAL PRIMARY KEY,
    incident_id INT REFERENCES incidents(id),
    technical_severity INT,
    business_impact INT,
    blast_radius INT,
    operational_context INT,
    total_score INT,
    risk_level VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE policy_decisions (
    id SERIAL PRIMARY KEY,
    incident_id INT REFERENCES incidents(id),
    decision VARCHAR(100),
    reason TEXT,
    requires_approval BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE replay_records (
    id SERIAL PRIMARY KEY,
    incident_id INT REFERENCES incidents(id),
    context_packet JSONB,
    model_input JSONB,
    model_output JSONB,
    policy_output JSONB,
    final_action JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

