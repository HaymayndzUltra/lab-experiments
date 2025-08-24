
### Phase 1 — Foundation

 Gumawa ng **product_owner_ai.mdc**

- Role: Define WHY, WHAT, backlog, priorities.
    
- Output schema: PO-BACKLOG v1.
    

 Gumawa ng **planning_ai.mdc**

- Role: Convert backlog → sprints & tasks.
    
- Output schema: PLAN-ROADMAP v1.
    

---

### Phase 2 — Execution Core

**Gumawa ng codegen_ai.mdc**

- Role: Implementation (design → code → tests).
    
- Output: Patch diffs, file list, unit test stubs.
    

 Gumawa ng **qa_ai.mdc**

- Role: Tester/Validator.
    
- Output: PASS|BLOCK + defect list, coverage deltas.
    

 Gumawa ng **mlops_ai.mdc**

- Role: Deployment & monitoring.
    
- Output: Deployment plan + rollback + health checks.
    

---

### Phase 3 — Support & Scaling

 **Gumawa ng documentation_ai.mdc**

- Role: Project docs, changelogs, summaries.
    
- Output: Markdown/structured docs.
    

 **Gumawa ng analyst_ai.mdc**

- Role: Critical reviewer (logical consistency, risks).
    
- Output: Analysis report + recommendations.
    

 **Gumawa ng memory_ai.mdc**

- Role: Session memory manager (single-writer policy, context sync, retention/archive).
    
- Output: Synced session snapshots + context diffs.
    

 **Gumawa ng observability_ai.mdc**

- Role: Monitor & forensic reporter.
    
- Output: Daily/weekly run summaries (top commands, failures, durations).
    

---

### Phase 4 — Orchestration

 **Gumawa ng rules_master_toggle.mdc**

- Purpose: Central ON/OFF toggle + trigger routing.
    
- Output: Defines which role responds per trigger.
    

 **Gumawa ng execution_orchestrator.mdc**

- Purpose: Handoff sequence (PO → Planning → CodeGen → QA → MLOps).
    
- Output: Session flow, gating rules, feedback loops.