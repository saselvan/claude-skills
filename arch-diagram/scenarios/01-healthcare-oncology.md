### Scenario 1: Healthcare Oncology Data Unification

**Audience:** C-suite + medical informatics leads  
**Intent:** Show how Databricks solves fragmented oncology data across regional labs  
**Canvas Size:** S (1200x700)

**Architecture:** Regional labs (A/B/C) + EHR (Epic/Cerner) → Auto Loader/Lakeflow Connect → Bronze/Silver/Gold medallion → Mosaic AI (biomarker prediction) + Databricks SQL → Research oncologists, clinical trial ops, RWE analytics, BI tools

**Talking Points:**
- Unified data from disparate labs — single source of truth
- HIPAA governance built-in via Unity Catalog (lineage, masking, audit)
- Trial-ready datasets reduce time-to-insight from months to days
- Mosaic AI enables predictive biomarker scoring on curated data

```xml
<mxfile>
  <diagram name="Healthcare Oncology Data Unification" id="oncology-arch-1">
    <mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1200" pageHeight="700">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- PLATFORM BANNER (Coral) -->
        <mxCell id="platform-banner" value="Data Intelligence Platform" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FF3621;fontColor=#FFFFFF;strokeColor=#FF3621;fontSize=14;fontStyle=1;verticalAlign=middle;" 
          vertex="1" parent="1">
          <mxGeometry x="360" y="20" width="520" height="40" as="geometry"/>
        </mxCell>
        
        <!-- DATA SOURCES ZONE (Left) -->
        <mxCell id="zone-sources" value="Data Sources" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#333333;dashed=0;" 
          vertex="1" parent="1">
          <mxGeometry x="20" y="80" width="160" height="480" as="geometry"/>
        </mxCell>
        
        <mxCell id="source-lab-a" value="Regional Lab A&#xa;Genomics&#xa;Pathology&#xa;Clinical" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8E8E8;fontColor=#333333;strokeColor=#666666;fontSize=10;" 
          vertex="1" parent="zone-sources">
          <mxGeometry x="20" y="40" width="120" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="source-lab-b" value="Regional Lab B&#xa;Genomics&#xa;Pathology&#xa;Clinical" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8E8E8;fontColor=#333333;strokeColor=#666666;fontSize=10;" 
          vertex="1" parent="zone-sources">
          <mxGeometry x="20" y="140" width="120" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="source-lab-c" value="Regional Lab C&#xa;Genomics&#xa;Pathology&#xa;Clinical" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8E8E8;fontColor=#333333;strokeColor=#666666;fontSize=10;" 
          vertex="1" parent="zone-sources">
          <mxGeometry x="20" y="240" width="120" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="source-epic" value="Epic EHR&#xa;Electronic Health Records" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8E8E8;fontColor=#333333;strokeColor=#666666;fontSize="10;" 
          vertex="1" parent="zone-sources">
          <mxGeometry x="20" y="340" width="120" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="source-cerner" value="Cerner EHR&#xa;Electronic Health Records" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8E8E8;fontColor=#333333;strokeColor=#666666;fontSize="10;" 
          vertex="1" parent="zone-sources">
          <mxGeometry x="20" y="410" width="120" height="50" as="geometry"/>
        </mxCell>
        
        <!-- CONNECTIVITY ZONE (Left-Center) -->
        <mxCell id="zone-connectivity" value="Connectivity" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#333333;dashed=0;" 
          vertex="1" parent="1">
          <mxGeometry x="200" y="80" width="140" height="480" as="geometry"/>
        </mxCell>
        
        <mxCell id="conn-autoloader" value="Auto Loader&#xa;HL7, DICOM, FHIR" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-connectivity">
          <mxGeometry x="20" y="100" width="100" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="conn-lakeflow" value="Lakeflow Connect&#xa;EHR Database&#xa;Extracts" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-connectivity">
          <mxGeometry x="20" y="360" width="100" height="60" as="geometry"/>
        </mxCell>
        
        <!-- PLATFORM ZONE (Center) -->
        <mxCell id="zone-platform" value="" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#FF3621;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=14;fontColor=#FF3621;dashed=0;" 
          vertex="1" parent="1">
          <mxGeometry x="360" y="80" width="520" height="480" as="geometry"/>
        </mxCell>
        
        <mxCell id="layer-bronze" value="Bronze&#xa;Raw HL7 messages,&#xa;DICOM images,&#xa;clinical notes" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#CD7F32;fontColor=#FFFFFF;strokeColor=#8B4513;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="40" y="60" width="160" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="layer-silver" value="Silver&#xa;De-identified,&#xa;FHIR-normalized&#xa;patient records" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#C0C0C0;fontColor=#000000;strokeColor=#808080;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="40" y="180" width="160" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="layer-gold" value="Gold&#xa;Patient cohorts,&#xa;biomarker profiles,&#xa;trial-ready datasets" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFD700;fontColor=#000000;strokeColor=#DAA520;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="40" y="300" width="160" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="comp-lakeflow-jobs" value="Lakeflow Jobs&#xa;(Orchestration)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="240" y="120" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="comp-mosaic" value="Mosaic AI&#xa;Biomarker prediction&#xa;Cohort scoring" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9B2D5E;fontColor=#FFFFFF;strokeColor=#7A2349;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="240" y="240" width="120" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="comp-dbsql" value="Databricks SQL&#xa;(Warehouse &amp; Analytics)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="240" y="360" width="120" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="comp-uc" value="Unity Catalog&#xa;(Discovery &amp; Governance)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1B3A4B;fontColor=#FFFFFF;strokeColor=#0F2530;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="400" y="200" width="90" height="70" as="geometry"/>
        </mxCell>
        
        <!-- CONSUMERS ZONE (Right) -->
        <mxCell id="zone-consumers" value="Consumers" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#333333;dashed=0;" 
          vertex="1" parent="1">
          <mxGeometry x="900" y="80" width="140" height="480" as="geometry"/>
        </mxCell>
        
        <mxCell id="consumer-research" value="Research&#xa;Oncologists" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8E8E8;fontColor=#333333;strokeColor=#666666;fontSize=10;" 
          vertex="1" parent="zone-consumers">
          <mxGeometry x="20" y="50" width="100" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="consumer-trial-ops" value="Clinical Trial&#xa;Operations" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8E8E8;fontColor=#333333;strokeColor=#666666;fontSize=10;" 
          vertex="1" parent="zone-consumers">
          <mxGeometry x="20" y="130" width="100" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="consumer-rwe" value="Real-World&#xa;Evidence Analytics" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8E8E8;fontColor=#333333;strokeColor=#666666;fontSize=10;" 
          vertex="1" parent="zone-consumers">
          <mxGeometry x="20" y="210" width="100" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="consumer-tableau" value="Tableau" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8E8E8;fontColor=#333333;strokeColor=#666666;fontSize=10;" 
          vertex="1" parent="zone-consumers">
          <mxGeometry x="20" y="310" width="100" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="consumer-powerbi" value="Power BI" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8E8E8;fontColor=#333333;strokeColor=#666666;fontSize=10;" 
          vertex="1" parent="zone-consumers">
          <mxGeometry x="20" y="370" width="100" height="40" as="geometry"/>
        </mxCell>
        
        <!-- GOVERNANCE BAR (Full Width, Dark Teal) -->
        <mxCell id="gov-bar" value="Governance — Unity Catalog: HIPAA compliance · Column-level masking · Lineage · Audit trail" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#1B3A4B;fontColor=#FFFFFF;strokeColor=#1B3A4B;fontSize=11;fontStyle=1;verticalAlign=middle;" 
          vertex="1" parent="1">
          <mxGeometry x="0" y="580" width="1200" height="50" as="geometry"/>
        </mxCell>
        
        <!-- FOUNDATION BAR (Coral) -->
        <mxCell id="foundation" value="Delta Lake · Iceberg · Apache Spark · Photon" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FF3621;fontColor=#FFFFFF;strokeColor=#FF3621;fontSize=11;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="360" y="640" width="520" height="40" as="geometry"/>
        </mxCell>
        
        <!-- NUMBERED STEP INDICATORS (Teal) -->
        <mxCell id="step-1" value="1" 
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#00A972;fontSize=12;fontStyle=1;aspect=fixed;" 
          vertex="1" parent="1">
          <mxGeometry x="100" y="50" width="28" height="28" as="geometry"/>
        </mxCell>
        
        <mxCell id="step-2" value="2" 
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#00A972;fontSize=12;fontStyle=1;aspect=fixed;" 
          vertex="1" parent="1">
          <mxGeometry x="270" y="50" width="28" height="28" as="geometry"/>
        </mxCell>
        
        <mxCell id="step-3" value="3" 
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#00A972;fontSize=12;fontStyle=1;aspect=fixed;" 
          vertex="1" parent="1">
          <mxGeometry x="480" y="50" width="28" height="28" as="geometry"/>
        </mxCell>
        
        <mxCell id="step-4" value="4" 
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#00A972;fontSize=12;fontStyle=1;aspect=fixed;" 
          vertex="1" parent="1">
          <mxGeometry x="550" y="50" width="28" height="28" as="geometry"/>
        </mxCell>
        
        <mxCell id="step-5" value="5" 
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#00A972;fontSize=12;fontStyle=1;aspect=fixed;" 
          vertex="1" parent="1">
          <mxGeometry x="620" y="50" width="28" height="28" as="geometry"/>
        </mxCell>
        
        <mxCell id="step-6" value="6" 
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#00A972;fontSize=12;fontStyle=1;aspect=fixed;" 
          vertex="1" parent="1">
          <mxGeometry x="970" y="50" width="28" height="28" as="geometry"/>
        </mxCell>
        
        <!-- EDGES / ARROWS (Labeled) -->
        <mxCell id="edge-lab-autoloader" value="HL7, DICOM, FHIR" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="source-lab-a" target="conn-autoloader" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-labb-autoloader" value="HL7, DICOM, FHIR" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="source-lab-b" target="conn-autoloader" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-labc-autoloader" value="HL7, DICOM, FHIR" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="source-lab-c" target="conn-autoloader" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-epic-lakeflow" value="Database CDC" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="source-epic" target="conn-lakeflow" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-cerner-lakeflow" value="Database CDC" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="source-cerner" target="conn-lakeflow" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-autoloader-bronze" value="Streaming ingest" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="conn-autoloader" target="layer-bronze" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-lakeflow-bronze" value="Batch ETL" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="conn-lakeflow" target="layer-bronze" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-bronze-silver" value="Cleanse &amp; normalize" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="layer-bronze" target="layer-silver" parent="zone-platform">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-silver-gold" value="Aggregate &amp; enrich" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="layer-silver" target="layer-gold" parent="zone-platform">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-gold-research" value="Cohort data" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="layer-gold" target="consumer-research" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-gold-trialops" value="Trial-ready datasets" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="layer-gold" target="consumer-trial-ops" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-gold-rwe" value="RWE datasets" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="layer-gold" target="consumer-rwe" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-dbsql-tableau" value="SQL endpoint" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="comp-dbsql" target="consumer-tableau" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-dbsql-powerbi" value="SQL endpoint" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="comp-dbsql" target="consumer-powerbi" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```


---

