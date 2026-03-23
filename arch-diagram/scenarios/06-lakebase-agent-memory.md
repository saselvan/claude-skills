### Scenario 6: Lakebase AI Agent Memory Architecture

**Audience:** Enterprise architects evaluating agentic AI workloads  
**Intent:** Show how Lakebase provides structured memory for AI agents  
**Canvas Size:** L (1800x1100)

**Architecture:**
- Zone 1 (Left): Data Sources — user interactions, enterprise systems, external APIs
- Zone 2 (Left-Center): Agent Runtime — LangGraph/OpenAI Agents SDK on Databricks Apps, Mosaic AI Model Serving, Agent Tools (UC Function Calling, Mosaic AI Vector Search as tool NOT memory)
- Zone 3 (Center): Lakebase Memory Layer — Short-term (thread_id checkpoints), Long-term (JSONB user profiles), Semantic (pgvector episodic recall)
- Zone 4 (Bottom-Center): Lakehouse Feedback Loop — agent data → Delta → Agent Evaluation → Fine-tuning → Databricks SQL
- Zone 5 (Bottom): Governance — Unity Catalog (full width)
- Zone 6 (Right): Agent Surfaces — Databricks Apps, AI/BI Genie, Slack/Teams, MLflow

**Critical architectural distinction:** Mosaic AI Vector Search is an agent TOOL for enterprise knowledge retrieval (RAG), NOT memory. Lakebase semantic memory (pgvector) stores the agent's OWN past interaction embeddings.

```xml
<mxfile>
  <diagram name="Lakebase AI Agent Memory" id="lakebase-memory-1">
    <mxGraphModel dx="1800" dy="1100" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1800" pageHeight="1100">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <mxCell id="platform-boundary" value="Data Intelligence Platform" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#FF3621;strokeWidth=3;verticalAlign=top;fontStyle=1;fontSize=16;fontColor=#FF3621;dashed=0;" 
          vertex="1" parent="1">
          <mxGeometry x="200" y="40" width="900" height="900" as="geometry"/>
        </mxCell>

        <mxCell id="zone-sources" value="Data Sources" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=13;fontColor=#333333;dashed=1;" 
          vertex="1" parent="1">
          <mxGeometry x="20" y="150" width="160" height="320" as="geometry"/>
        </mxCell>

        <mxCell id="source-user" value="User Interactions&#xa;Chat messages&#xa;Voice commands" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#666666;fontSize=10;fontColor=#333333;" 
          vertex="1" parent="1">
          <mxGeometry x="35" y="180" width="130" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="source-enterprise" value="Enterprise Systems&#xa;CRM · ERP · HRIS" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#666666;fontSize=10;fontColor=#333333;" 
          vertex="1" parent="1">
          <mxGeometry x="35" y="270" width="130" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="source-api" value="External APIs&#xa;Search · Weather&#xa;Market data" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#666666;fontSize=10;fontColor=#333333;" 
          vertex="1" parent="1">
          <mxGeometry x="35" y="360" width="130" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="zone-runtime" value="Agent Runtime" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#9B2D5E;strokeColor=#7A2449;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=13;fontColor=#FFFFFF;dashed=0;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="30" y="60" width="260" height="420" as="geometry"/>
        </mxCell>

        <mxCell id="runtime-framework" value="LangGraph / OpenAI Agents SDK&#xa;on Databricks Apps" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9B2D5E;strokeColor=#7A2449;fontSize=11;fontColor=#FFFFFF;fontStyle=1;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="50" y="90" width="220" height="60" as="geometry"/>
        </mxCell>

        <mxCell id="runtime-model" value="Mosaic AI&#xa;Model Serving" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9B2D5E;strokeColor=#7A2449;fontSize=11;fontColor=#FFFFFF;fontStyle=1;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="50" y="170" width="220" height="50" as="geometry"/>
        </mxCell>

        <mxCell id="tool-uc" value="Unity Catalog&#xa;Function Calling" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;strokeColor=#0D5A8E;fontSize=10;fontColor=#FFFFFF;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="70" y="270" width="180" height="45" as="geometry"/>
        </mxCell>

        <mxCell id="tool-vector" value="Mosaic AI&#xa;Vector Search&#xa;(Retrieval Tool)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;strokeColor=#0D5A8E;fontSize=10;fontColor=#FFFFFF;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="70" y="330" width="180" height="50" as="geometry"/>
        </mxCell>

        <mxCell id="tool-other" value="External Tool Calls&#xa;APIs · Web Search" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;strokeColor=#0D5A8E;fontSize=10;fontColor=#FFFFFF;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="70" y="395" width="180" height="35" as="geometry"/>
        </mxCell>

        <mxCell id="zone-memory" value="Lakebase Memory Layer (PostgreSQL + pgvector)" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#9B2D5E;strokeColor=#7A2449;strokeWidth=3;verticalAlign=top;fontStyle=1;fontSize=14;fontColor=#FFFFFF;dashed=0;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="320" y="60" width="400" height="420" as="geometry"/>
        </mxCell>

        <mxCell id="memory-short" value="Short-Term Memory&#xa;(Thread-scoped)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9B2D5E;strokeColor=#7A2449;fontSize=12;fontColor=#FFFFFF;fontStyle=1;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="345" y="100" width="160" height="130" as="geometry"/>
        </mxCell>

        <mxCell id="short-checkpoints" value="• Conversation checkpoints&#xa;• Session state&#xa;• Tool call history&#xa;• thread_id scoped" 
          style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;whiteSpace=wrap;fontSize=10;fontColor=#FFFFFF;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="355" y="135" width="140" height="85" as="geometry"/>
        </mxCell>

        <mxCell id="memory-long" value="Long-Term Memory&#xa;(User-scoped)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9B2D5E;strokeColor=#7A2449;fontSize=12;fontColor=#FFFFFF;fontStyle=1;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="535" y="100" width="160" height="130" as="geometry"/>
        </mxCell>

        <mxCell id="long-profiles" value="• User profiles&#xa;• Preferences&#xa;• Cross-session insights&#xa;• JSONB lookups" 
          style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;whiteSpace=wrap;fontSize=10;fontColor=#FFFFFF;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="545" y="135" width="140" height="85" as="geometry"/>
        </mxCell>

        <mxCell id="memory-semantic" value="Semantic Memory&#xa;(pgvector embeddings)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9B2D5E;strokeColor=#7A2449;fontSize=12;fontColor=#FFFFFF;fontStyle=1;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="345" y="260" width="350" height="180" as="geometry"/>
        </mxCell>

        <mxCell id="semantic-details" value="Episodic Recall Storage&#xa;&#xa;• Agent's own past interaction embeddings&#xa;• Resolution patterns &amp; successful strategies&#xa;• Similar case retrieval via vector similarity&#xa;• Learned preferences from conversation history&#xa;&#xa;Enables: &quot;I've seen this before – here's what worked&quot;" 
          style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;whiteSpace=wrap;fontSize=10;fontColor=#FFFFFF;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="360" y="295" width="320" height="130" as="geometry"/>
        </mxCell>

        <mxCell id="zone-feedback" value="Lakehouse Feedback Loop" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#137CBD;strokeColor=#0D5A8E;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=13;fontColor=#FFFFFF;dashed=0;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="200" y="510" width="640" height="300" as="geometry"/>
        </mxCell>

        <mxCell id="feedback-delta" value="Agent Data&#xa;Auto-sync to Delta" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;strokeColor=#0D5A8E;fontSize=11;fontColor=#FFFFFF;fontStyle=1;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="230" y="550" width="140" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="feedback-eval" value="Agent&#xa;Evaluation" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;strokeColor=#0D5A8E;fontSize=11;fontColor=#FFFFFF;fontStyle=1;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="410" y="550" width="120" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="feedback-finetune" value="Model&#xa;Fine-tuning" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;strokeColor=#0D5A8E;fontSize=11;fontColor=#FFFFFF;fontStyle=1;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="570" y="550" width="120" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="feedback-sql" value="Databricks SQL&#xa;Analytics" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;strokeColor=#0D5A8E;fontSize=11;fontColor=#FFFFFF;fontStyle=1;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="720" y="550" width="100" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="feedback-return" value="Insights feed back&#xa;to memory layer" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#00A972;strokeColor=#008F5F;fontSize=10;fontColor=#FFFFFF;fontStyle=1;" 
          vertex="1" parent="platform-boundary">
          <mxGeometry x="440" y="650" width="160" height="50" as="geometry"/>
        </mxCell>

        <mxCell id="gov-bar" value="Governance — Unity Catalog&#xa;Access control · Lineage · Audit · PII masking · Discovery" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#1B3A4B;fontColor=#FFFFFF;strokeColor=#1B3A4B;fontSize=12;fontStyle=1;verticalAlign=middle;" 
          vertex="1" parent="1">
          <mxGeometry x="0" y="960" width="1800" height="50" as="geometry"/>
        </mxCell>

        <mxCell id="zone-surfaces" value="Agent Surfaces" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=13;fontColor=#333333;dashed=1;" 
          vertex="1" parent="1">
          <mxGeometry x="1150" y="150" width="160" height="320" as="geometry"/>
        </mxCell>

        <mxCell id="surface-apps" value="Databricks Apps&#xa;(Custom UI)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#666666;fontSize=10;fontColor=#333333;" 
          vertex="1" parent="1">
          <mxGeometry x="1165" y="180" width="130" height="55" as="geometry"/>
        </mxCell>

        <mxCell id="surface-genie" value="AI/BI Genie&#xa;(NL Interface)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#666666;fontSize=10;fontColor=#333333;" 
          vertex="1" parent="1">
          <mxGeometry x="1165" y="255" width="130" height="55" as="geometry"/>
        </mxCell>

        <mxCell id="surface-chat" value="Slack / Teams&#xa;(Chat Integration)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#666666;fontSize=10;fontColor=#333333;" 
          vertex="1" parent="1">
          <mxGeometry x="1165" y="330" width="130" height="55" as="geometry"/>
        </mxCell>

        <mxCell id="surface-mlflow" value="MLflow&#xa;(Experiment Tracking)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#666666;fontSize=10;fontColor=#333333;" 
          vertex="1" parent="1">
          <mxGeometry x="1165" y="405" width="130" height="45" as="geometry"/>
        </mxCell>

        <mxCell id="foundation" value="Delta Lake · Iceberg · Apache Spark · Photon · Lakebase (pgvector)" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FF3621;fontColor=#FFFFFF;strokeColor=#FF3621;fontSize=12;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="0" y="1020" width="1800" height="45" as="geometry"/>
        </mxCell>

        <mxCell id="edge-source-to-runtime" value="Input events" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;strokeColor=#666666;strokeWidth=1.5;" 
          edge="1" source="source-user" target="runtime-framework" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="edge-runtime-to-short" value="Save checkpoint" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#9B2D5E;fontSize=10;strokeColor=#9B2D5E;strokeWidth=2;" 
          edge="1" source="runtime-framework" target="memory-short" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="edge-runtime-to-long" value="Fetch user profile" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#9B2D5E;fontSize=10;strokeColor=#9B2D5E;strokeWidth=2;" 
          edge="1" source="runtime-model" target="memory-long" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="edge-runtime-to-semantic" value="Recall similar interactions" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#9B2D5E;fontSize=10;strokeColor=#9B2D5E;strokeWidth=2;" 
          edge="1" source="runtime-framework" target="memory-semantic" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="edge-tool-vector-call" value="Enterprise knowledge retrieval" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#137CBD;fontSize=10;strokeColor=#137CBD;strokeWidth=1.5;" 
          edge="1" source="runtime-framework" target="tool-vector" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="edge-runtime-to-apps" value="Agent response" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;strokeColor=#666666;strokeWidth=1.5;" 
          edge="1" source="runtime-framework" target="surface-apps" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```


---

