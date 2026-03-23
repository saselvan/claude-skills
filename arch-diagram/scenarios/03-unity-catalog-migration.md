### Scenario 3: Unity Catalog Migration (Before/After)

**Audience:** Enterprise architects, data governance team  
**Intent:** Show before/after, governance gains, compliance alignment  
**Canvas Size:** S (1200x700)

**Architecture:** Before (Legacy Data Lake with S3 folder chaos) → Migration Path (Assess→Design→Migrate→Validate) → After (Databricks Lakehouse + Unity Catalog with organized catalogs/schemas)

**Talking Points:**
- Phased migration (no big-bang cut-over)
- Lineage + audit trails for compliance officers
- Data quality expectations in Lakeflow Jobs
- Reduced shadow IT (self-service governance)

```xml
<mxfile>
  <diagram name="Unity Catalog Migration" id="uc-migration-1">
    <mxGraphModel dx="1200" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1200" pageHeight="700">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <mxCell id="title" value="Unity Catalog Migration: Legacy Data Lake → Databricks Lakehouse" 
          style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=16;fontStyle=1;fontColor=#333333;" 
          vertex="1" parent="1">
          <mxGeometry x="0" y="10" width="1200" height="30" as="geometry"/>
        </mxCell>
        
        <mxCell id="zone-before" value="BEFORE — Legacy Data Lake" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFE6E6;strokeColor=#CC0000;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=13;fontColor=#CC0000;dashed=0;" 
          vertex="1" parent="1">
          <mxGeometry x="40" y="60" width="320" height="420" as="geometry"/>
        </mxCell>
        
        <mxCell id="before-s3" value="AWS S3" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF9900;fontColor=#FFFFFF;strokeColor=#FF8C00;fontSize=12;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="80" y="100" width="240" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="before-folder1" value="/data/raw/...&#xa;(unstructured chaos)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontColor=#333333;strokeColor=#999999;fontSize=10;" 
          vertex="1" parent="1">
          <mxGeometry x="80" y="170" width="100" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="before-folder2" value="/data/processed/...&#xa;(stale copies)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontColor=#333333;strokeColor=#999999;fontSize=10;" 
          vertex="1" parent="1">
          <mxGeometry x="220" y="170" width="100" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="before-problems" value="PROBLEMS&#xa;• Orphaned datasets&#xa;• No lineage tracking&#xa;• Ad-hoc access (S3 policies)&#xa;• Compliance gaps&#xa;• Data silos" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontColor=#CC0000;strokeColor=#CC0000;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="80" y="320" width="240" height="100" as="geometry"/>
        </mxCell>
        
        <mxCell id="zone-migration" value="Migration Path" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=13;fontColor=#333333;dashed=0;" 
          vertex="1" parent="1">
          <mxGeometry x="400" y="60" width="200" height="420" as="geometry"/>
        </mxCell>
        
        <mxCell id="mig-assess" value="1. ASSESS&#xa;Data inventory,&#xa;ownership mapping" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#008F5F;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="425" y="90" width="150" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="mig-design" value="2. DESIGN&#xa;Catalog/schema&#xa;hierarchy design" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#008F5F;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="425" y="180" width="150" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="mig-migrate" value="3. MIGRATE&#xa;External → UC managed&#xa;via Lakeflow Jobs" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#008F5F;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="425" y="270" width="150" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="mig-validate" value="4. VALIDATE&#xa;Lineage verification,&#xa;access validation" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#008F5F;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="425" y="360" width="150" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="zone-after" value="AFTER — Databricks Lakehouse + Unity Catalog" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#E6FFE6;strokeColor=#00AA00;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=13;fontColor=#00AA00;dashed=0;" 
          vertex="1" parent="1">
          <mxGeometry x="640" y="60" width="520" height="420" as="geometry"/>
        </mxCell>
        
        <mxCell id="after-uc" value="Unity Catalog" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1B3A4B;fontColor=#FFFFFF;strokeColor=#0F2530;fontSize=12;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="680" y="90" width="200" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="after-metastore" value="Metastore" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=10;" 
          vertex="1" parent="1">
          <mxGeometry x="900" y="90" width="100" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="schema-raw" value="raw_fhir&#xa;(Bronze)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#CD7F32;fontColor=#FFFFFF;strokeColor=#8B4513;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="700" y="190" width="100" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="schema-cleaned" value="cleaned&#xa;(Silver)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#C0C0C0;fontColor=#000000;strokeColor=#808080;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="850" y="190" width="100" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="schema-ml" value="ml_features&#xa;(Gold)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFD700;fontColor=#000000;strokeColor=#B8860B;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="1000" y="190" width="100" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="svc-lakeflow" value="Lakeflow Jobs" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="700" y="325" width="90" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="svc-dlt" value="Delta Live Tables" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="820" y="325" width="100" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="svc-sql" value="Databricks SQL" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="950" y="325" width="100" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="after-benefits" value="BENEFITS&#xa;✓ Full lineage tracking&#xa;✓ Fine-grained RBAC&#xa;✓ Audit logs, column masking&#xa;✓ HIPAA, GDPR ready&#xa;✓ Tag-based policies&#xa;✓ Self-service discovery" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E6FFE6;fontColor=#00AA00;strokeColor=#00AA00;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="40" y="500" width="200" height="120" as="geometry"/>
        </mxCell>
        
        <mxCell id="gov-bar" value="Governance — Unity Catalog | Access control · PII masking · Lineage · Audit trail · Tag-based policies" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#1B3A4B;fontColor=#FFFFFF;strokeColor=#1B3A4B;fontSize=11;fontStyle=1;verticalAlign=middle;" 
          vertex="1" parent="1">
          <mxGeometry x="0" y="500" width="1200" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="foundation" value="Delta Lake · Iceberg · Apache Spark · Photon · Unity Catalog" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FF3621;fontColor=#FFFFFF;strokeColor=#FF3621;fontSize=11;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="0" y="560" width="1200" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-before-assess" value="Identify stale/duplicate" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="zone-before" target="mig-assess" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-assess-design" value="Map to UC hierarchy" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="mig-assess" target="mig-design" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-design-migrate" value="Plan migration" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="mig-design" target="mig-migrate" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-migrate-validate" value="Execute ETL" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="mig-migrate" target="mig-validate" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-validate-after" value="Golden-path ingestion" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="mig-validate" target="zone-after" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```


---

