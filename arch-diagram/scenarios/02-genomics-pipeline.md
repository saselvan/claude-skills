### Scenario 2: Genomics Data Pipeline for Precision Medicine

**Audience:** Data engineering + research biology team  
**Intent:** Show Lakeflow + Mosaic AI for variant calling, annotation, and model scoring  
**Canvas Size:** M (1500x900)

**Architecture:** Sequencers (NextSeq, NovaSeq, PacBio) + EHR → Auto Loader → Lakeflow Jobs (variant calling: QC, alignment, annotation) → S3 Data Lake (Bronze/Silver/Gold) → Databricks SQL + Mosaic AI → Feature Store → Model Serving → Clinical Reporting App → Oncologist

**Talking Points:**
- End-to-end reproducibility (Mosaic AI + Lakeflow Jobs for audit trail)
- Real-time API for clinical decision support
- Feature Store reduces model deployment latency
- Unity Catalog governs patient data at every step

```xml
<mxfile>
  <diagram name="Genomics Data Pipeline" id="genomics-arch-1">
    <mxGraphModel dx="1500" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1500" pageHeight="900">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <mxCell id="platform-banner" value="Data Intelligence Platform" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FF3621;fontColor=#FFFFFF;strokeColor=#FF3621;fontSize=14;fontStyle=1;verticalAlign=middle;" 
          vertex="1" parent="1">
          <mxGeometry x="400" y="20" width="600" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="person-researcher" value="Research Biologist&#xa;(Runs variant analysis,&#xa;trains models)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E1F5FE;fontColor=#01579B;strokeColor=#0288D1;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="50" y="20" width="140" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="person-clinician" value="Oncologist&#xa;(Makes treatment&#xa;decisions)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E1F5FE;fontColor=#01579B;strokeColor=#0288D1;fontSize=10;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="1320" y="20" width="130" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="zone-sources" value="Data Sources" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#333333;dashed=0;" 
          vertex="1" parent="1">
          <mxGeometry x="30" y="100" width="160" height="380" as="geometry"/>
        </mxCell>
        
        <mxCell id="source-sequencers" value="Sequencers&#xa;NextSeq, NovaSeq,&#xa;PacBio" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8E8E8;fontColor=#333333;strokeColor=#666666;fontSize=10;" 
          vertex="1" parent="zone-sources">
          <mxGeometry x="20" y="50" width="120" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="source-ehr" value="EHR System&#xa;Epic, Cerner,&#xa;InterSystems" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8E8E8;fontColor=#333333;strokeColor=#666666;fontSize=10;" 
          vertex="1" parent="zone-sources">
          <mxGeometry x="20" y="150" width="120" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="zone-connectivity" value="Connectivity" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#333333;dashed=0;" 
          vertex="1" parent="1">
          <mxGeometry x="220" y="100" width="150" height="380" as="geometry"/>
        </mxCell>
        
        <mxCell id="conn-autoloader" value="Auto Loader&#xa;Ingests FASTQ,&#xa;BAM, VCF files" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-connectivity">
          <mxGeometry x="25" y="100" width="100" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="zone-platform" value="" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#FF3621;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=14;fontColor=#FF3621;dashed=0;" 
          vertex="1" parent="1">
          <mxGeometry x="400" y="70" width="600" height="600" as="geometry"/>
        </mxCell>
        
        <mxCell id="comp-lakeflow" value="Lakeflow Jobs&#xa;Variant calling pipeline:&#xa;QC, alignment, annotation" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="40" y="60" width="140" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="layer-bronze" value="Bronze&#xa;Raw sequencing files&#xa;(FASTQ, BAM)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#CD7F32;fontColor=#FFFFFF;strokeColor=#8B4513;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="40" y="160" width="140" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="layer-silver" value="Silver&#xa;Aligned reads,&#xa;processed BAM" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#C0C0C0;fontColor=#000000;strokeColor=#808080;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="220" y="160" width="140" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="layer-gold" value="Gold&#xa;Annotated VCF,&#xa;variant calls" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFD700;fontColor=#000000;strokeColor=#B8860B;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="400" y="160" width="140" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="comp-dbsql" value="Databricks SQL&#xa;Exploratory analysis,&#xa;cohort queries" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="40" y="280" width="140" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="comp-mosaic" value="Mosaic AI&#xa;Experiment tracking:&#xa;variant effect prediction" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9B2D5E;fontColor=#FFFFFF;strokeColor=#7A2349;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="220" y="280" width="140" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="comp-featurestore" value="Feature Store&#xa;Pre-computed variant&#xa;impact scores, risk factors" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9B2D5E;fontColor=#FFFFFF;strokeColor=#7A2349;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="400" y="280" width="140" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="comp-serving" value="Model Serving&#xa;Real-time variant&#xa;interpretation API" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9B2D5E;fontColor=#FFFFFF;strokeColor=#7A2349;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="220" y="400" width="140" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="comp-uc" value="Unity Catalog&#xa;Data governance:&#xa;lineage, access, PII" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1B3A4B;fontColor=#FFFFFF;strokeColor=#0F2530;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="430" y="400" width="130" height="70" as="geometry"/>
        </mxCell>
        
        <mxCell id="zone-consumers" value="Consumers" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#666666;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#333333;dashed=0;" 
          vertex="1" parent="1">
          <mxGeometry x="1040" y="100" width="160" height="380" as="geometry"/>
        </mxCell>
        
        <mxCell id="consumer-app" value="Clinical Reporting&#xa;App&#xa;Treatment recommendation&#xa;engine" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8E8E8;fontColor=#333333;strokeColor=#666666;fontSize=10;" 
          vertex="1" parent="zone-consumers">
          <mxGeometry x="20" y="150" width="120" height="80" as="geometry"/>
        </mxCell>
        
        <mxCell id="gov-bar" value="Governance — Unity Catalog: Lineage · Access control · PII masking · Audit logs" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#1B3A4B;fontColor=#FFFFFF;strokeColor=#1B3A4B;fontSize=11;fontStyle=1;verticalAlign=middle;" 
          vertex="1" parent="1">
          <mxGeometry x="0" y="700" width="1500" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="foundation" value="Delta Lake · Iceberg · Apache Spark · Photon" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FF3621;fontColor=#FFFFFF;strokeColor=#FF3621;fontSize=11;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="400" y="760" width="600" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-seq-autoloader" value="FASTQ, BAM files" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="source-sequencers" target="conn-autoloader" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-autoloader-lakeflow" value="Ingest" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="conn-autoloader" target="comp-lakeflow" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-lakeflow-bronze" value="Store raw" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="comp-lakeflow" target="layer-bronze" parent="zone-platform">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-bronze-silver" value="Alignment" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="layer-bronze" target="layer-silver" parent="zone-platform">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-silver-gold" value="Variant calling" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="layer-silver" target="layer-gold" parent="zone-platform">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-researcher-sql" value="Explore, prototype" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="person-researcher" target="comp-dbsql" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-researcher-mosaic" value="Track experiments" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="person-researcher" target="comp-mosaic" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-mosaic-feature" value="Log variants → features" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="comp-mosaic" target="comp-featurestore" parent="zone-platform">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-feature-serving" value="Serve predictions" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="comp-featurestore" target="comp-serving" parent="zone-platform">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-serving-app" value="REST API: variant impact scores" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="comp-serving" target="consumer-app" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-app-clinician" value="Clinical report: actionable insights" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="consumer-app" target="person-clinician" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```


---

