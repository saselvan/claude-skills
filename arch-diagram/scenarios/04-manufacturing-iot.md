### Scenario 4: Manufacturing Quality Control (IoT → Real-Time Analytics)

**Audience:** Operations + quality teams  
**Intent:** Show real-time defect detection, batch traceability  
**Canvas Size:** M (1500x900)

**Architecture:** IoT Sensors (Temp, Pressure, Vibration, Humidity) → Kinesis Streams → Tumbling Windows → Bronze/Silver/Gold → Lakeflow Jobs + DLT Expectations → Mosaic AI Anomaly Detection → Live Dashboard + Alerts → Operations Team, Quality Manager, Regulatory Reports

**Talking Points:**
- Real-time defect detection (minutes, not hours)
- Full batch traceability for recalls
- Structured streaming for high-frequency data
- Anomaly detection reduces scrap/rework

```xml
<mxfile>
  <diagram name="Manufacturing Quality Control" id="mqc-iot-1">
    <mxGraphModel dx="1500" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1500" pageHeight="900">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <mxCell id="step-1" value="1" 
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#00A972;fontSize=12;fontStyle=1;aspect=fixed;" 
          vertex="1" parent="1">
          <mxGeometry x="10" y="180" width="28" height="28" as="geometry"/>
        </mxCell>
        <mxCell id="step-2" value="2" 
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#00A972;fontSize=12;fontStyle=1;aspect=fixed;" 
          vertex="1" parent="1">
          <mxGeometry x="230" y="180" width="28" height="28" as="geometry"/>
        </mxCell>
        <mxCell id="step-3" value="3" 
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#00A972;fontSize=12;fontStyle=1;aspect=fixed;" 
          vertex="1" parent="1">
          <mxGeometry x="460" y="180" width="28" height="28" as="geometry"/>
        </mxCell>
        <mxCell id="step-4" value="4" 
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#00A972;fontSize=12;fontStyle=1;aspect=fixed;" 
          vertex="1" parent="1">
          <mxGeometry x="1050" y="180" width="28" height="28" as="geometry"/>
        </mxCell>
        <mxCell id="step-5" value="5" 
          style="ellipse;whiteSpace=wrap;html=1;fillColor=#00A972;fontColor=#FFFFFF;strokeColor=#00A972;fontSize=12;fontStyle=1;aspect=fixed;" 
          vertex="1" parent="1">
          <mxGeometry x="1270" y="180" width="28" height="28" as="geometry"/>
        </mxCell>
        
        <mxCell id="zone-sources" value="IoT Sensors — Lines 1-10" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#999999;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=13;fontColor=#333333;" 
          vertex="1" parent="1">
          <mxGeometry x="0" y="100" width="180" height="320" as="geometry"/>
        </mxCell>
        
        <mxCell id="sensor-temp" value="Temperature&#xa;Sensors" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontColor=#333333;strokeColor=#666666;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-sources">
          <mxGeometry x="20" y="50" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="sensor-pressure" value="Pressure&#xa;Sensors" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontColor=#333333;strokeColor=#666666;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-sources">
          <mxGeometry x="20" y="120" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="sensor-vibration" value="Vibration&#xa;Sensors" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontColor=#333333;strokeColor=#666666;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-sources">
          <mxGeometry x="20" y="190" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="sensor-humidity" value="Humidity&#xa;Sensors" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontColor=#333333;strokeColor=#666666;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-sources">
          <mxGeometry x="20" y="260" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="zone-ingestion" value="Streaming Ingestion" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#999999;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=13;fontColor=#333333;" 
          vertex="1" parent="1">
          <mxGeometry x="220" y="100" width="180" height="320" as="geometry"/>
        </mxCell>
        
        <mxCell id="kinesis" value="Kinesis Streams" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-ingestion">
          <mxGeometry x="20" y="80" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="tumbling" value="Tumbling Windows&#xa;(1 min)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-ingestion">
          <mxGeometry x="20" y="160" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="auto-loader" value="Auto Loader" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-ingestion">
          <mxGeometry x="20" y="240" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="zone-platform" value="Data Intelligence Platform" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#FF3621;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=14;fontColor=#FF3621;" 
          vertex="1" parent="1">
          <mxGeometry x="440" y="60" width="560" height="600" as="geometry"/>
        </mxCell>
        
        <mxCell id="layer-bronze" value="Bronze&#xa;Raw sensor readings, timestamps" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#CD7F32;fontColor=#FFFFFF;strokeColor=#8B4513;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="40" y="60" width="200" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="layer-silver" value="Silver&#xa;Cleaned, windowed aggregates" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#C0C0C0;fontColor=#000000;strokeColor=#808080;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="40" y="160" width="200" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="layer-gold" value="Gold&#xa;Batch quality scores, SPC metrics" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFD700;fontColor=#000000;strokeColor=#B8860B;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="40" y="260" width="200" height="60" as="geometry"/>
        </mxCell>
        
        <mxCell id="lakeflow-jobs" value="Lakeflow Jobs" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="280" y="170" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="zone-mosaic" value="Mosaic AI" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#9B2D5E;strokeColor=#7A2449;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=12;fontColor=#FFFFFF;" 
          vertex="1" parent="zone-platform">
          <mxGeometry x="40" y="460" width="480" height="110" as="geometry"/>
        </mxCell>
        
        <mxCell id="anomaly-detection" value="Anomaly Detection" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontColor=#9B2D5E;strokeColor=#7A2449;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-mosaic">
          <mxGeometry x="30" y="40" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="model-serving" value="Model Serving" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontColor=#9B2D5E;strokeColor=#7A2449;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-mosaic">
          <mxGeometry x="200" y="40" width="120" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="feature-store" value="Feature Store&#xa;(Unity Catalog)" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontColor=#9B2D5E;strokeColor=#7A2449;fontSize=10;fontStyle=1;" 
          vertex="1" parent="zone-mosaic">
          <mxGeometry x="350" y="40" width="110" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="zone-serving" value="Real-Time Serving" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#999999;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=13;fontColor=#333333;" 
          vertex="1" parent="1">
          <mxGeometry x="1040" y="100" width="180" height="320" as="geometry"/>
        </mxCell>
        
        <mxCell id="live-dashboard" value="Live Dashboard" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#137CBD;fontColor=#FFFFFF;strokeColor=#0D5A8E;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-serving">
          <mxGeometry x="20" y="60" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="alerts" value="Real-Time Alerts" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFC107;fontColor=#000000;strokeColor=#FFA000;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-serving">
          <mxGeometry x="20" y="220" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="zone-consumers" value="Consumers" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#999999;strokeWidth=1;verticalAlign=top;fontStyle=1;fontSize=13;fontColor=#333333;" 
          vertex="1" parent="1">
          <mxGeometry x="1260" y="100" width="180" height="320" as="geometry"/>
        </mxCell>
        
        <mxCell id="consumer-ops" value="Operations Team" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontColor=#333333;strokeColor=#666666;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-consumers">
          <mxGeometry x="20" y="60" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="consumer-quality" value="Quality Manager" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontColor=#333333;strokeColor=#666666;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-consumers">
          <mxGeometry x="20" y="140" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="consumer-regulatory" value="Regulatory Reports" 
          style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;fontColor=#333333;strokeColor=#666666;fontSize=11;fontStyle=1;" 
          vertex="1" parent="zone-consumers">
          <mxGeometry x="20" y="220" width="140" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="gov-bar" value="Governance — Unity Catalog&#xa;Access control · Lineage · Audit · PII masking" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#1B3A4B;fontColor=#FFFFFF;strokeColor=#1B3A4B;fontSize=11;fontStyle=1;verticalAlign=middle;" 
          vertex="1" parent="1">
          <mxGeometry x="0" y="700" width="1500" height="50" as="geometry"/>
        </mxCell>
        
        <mxCell id="foundation" value="Delta Lake · Iceberg · Apache Spark · Photon" 
          style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FF3621;fontColor=#FFFFFF;strokeColor=#FF3621;fontSize=11;fontStyle=1;" 
          vertex="1" parent="1">
          <mxGeometry x="440" y="760" width="560" height="40" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-1" value="1,000 msg/sec" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;strokeColor=#666666;" 
          edge="1" source="zone-sources" target="zone-ingestion" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-2" value="Structured streaming" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;strokeColor=#666666;" 
          edge="1" source="zone-ingestion" target="zone-platform" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-bronze-silver" value="DLT expectations" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="layer-bronze" target="layer-silver" parent="zone-platform">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-silver-gold" value="Hourly batch" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=9;strokeColor=#666666;" 
          edge="1" source="layer-silver" target="layer-gold" parent="zone-platform">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-3" value="Sub-second queries" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;strokeColor=#666666;" 
          edge="1" source="zone-platform" target="zone-serving" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        
        <mxCell id="edge-4" value="REST API, Web UI, PDF" 
          style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jetSize=auto;html=1;fontColor=#666666;fontSize=10;strokeColor=#666666;" 
          edge="1" source="zone-serving" target="zone-consumers" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```


---

