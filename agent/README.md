# 🤖 AI Agent: Graph-Based Subtitle Improvement

## **Architecture Overview**

This AI agent uses a **graph-based architecture** with:
- **Nodes**: Processing steps
- **Edges**: Conditional transitions
- **Stop Conditions**: Success or max iterations
- **Resolver**: Orchestrates execution until problem solved

```
┌──────────────────────────────────────────────────────────┐
│                    GRAPH ARCHITECTURE                    │
└──────────────────────────────────────────────────────────┘

        START
          ↓
    [Analyze Target] ← Analyze chinese_sample.jpg (once)
          ↓
          ┌─────────────────────────────┐
          │   ITERATION LOOP            │
          │                             │
    [Generate Video] ← Create with parameters
          ↓
    [Take Screenshot] ← Capture frame @ 5sec
          ↓
    [Analyze Current] ← OCR analysis
          ↓
    [Compare] ← Score vs target
          ↓
          │
    ┌─────┴─────┐
    │   EDGES   │ Check stop conditions
    └─────┬─────┘
          │
    ┌─────┴─────────────────────────┐
    │                               │
 Score ≥ 95?                 Iteration ≥ 7?
    │ YES                           │ YES
    ↓                               ↓
[STOP: Success]              [STOP: Max Iterations]
    │                               │
    NO                              NO
    ↓                               ↓
[Adjust Parameters] ← Smart adjustment
    │
    └──────→ Loop back to [Generate Video]
```

## **Configuration (All Configurable)**

```python
config = AgentConfig(
    max_iterations=7,              # Stop after 7 tries
    success_threshold=95.0,        # Score needed to succeed
    comparison_weights={           # How to weight scores
        'clarity': 0.4,           # 40% weight on OCR confidence
        'position': 0.3,          # 30% weight on position match
        'size': 0.3               # 30% weight on size match
    },
    font_size_range=[28-40],      # Font sizes to try
    stroke_width_range=[1-3],     # Stroke widths to try
    position_range=[0.60-0.70]    # Vertical positions to try
)
```

## **Node Types**

| Node | Purpose | Input | Output |
|------|---------|-------|--------|
| **Analyze Target** | Extract metrics from chinese_sample.jpg | target image | target_metrics |
| **Generate Video** | Create video with subtitles | parameters | video file |
| **Take Screenshot** | Capture frame from video | video | screenshot |
| **Analyze Current** | OCR analysis of screenshot | screenshot | current_metrics |
| **Validate Chinese** | Check if Chinese chars present | current_metrics | validation result |
| **Compare** | Score current vs target | both metrics | comparison scores |
| **Adjust Parameters** | Smart parameter tuning | comparison | new parameters |
| **Stop Success** | Success threshold reached | score | DONE ✅ |
| **Stop Max Iterations** | Max tries reached | iteration count | DONE ⏹️ |
| **Stop Error** | No Chinese detected | validation | ERROR ❌ |

## **Edge Conditions**

Edges determine flow between nodes:

```python
# Edge 1: Success condition
if overall_score >= 95.0:
    → STOP: Success! 🎉

# Edge 2: Max iterations condition  
elif iteration >= 7:
    → STOP: Max iterations reached ⏹️

# Edge 3: Continue condition
else:
    → Adjust Parameters → Generate Next Video
```

## **Resolver**

The **Resolver** orchestrates the entire graph:

1. **Initialize**: Load config, create nodes
2. **Execute**: Run nodes in sequence
3. **Check Edges**: Evaluate stop conditions
4. **Iterate**: Loop until stopped
5. **Report**: Save results and print summary

## **Quick Start**

### **Run with Default Config (7 iterations, 95% threshold)**

```powershell
cd D:\video-agent\agent
python auto_improve_subtitles.py
```

### **Customize Configuration**

Edit `auto_improve_subtitles.py` line ~560:

```python
config = AgentConfig(
    max_iterations=10,          # Try up to 10 times
    success_threshold=90.0,     # Lower threshold
    comparison_weights={
        'clarity': 0.5,         # More weight on clarity
        'position': 0.25,
        'size': 0.25
    }
)
```

## **Example Output**

```
🤖 AI AGENT: Graph-Based Subtitle Improvement
============================================================

🤖 RESOLVER: Starting Graph Execution
============================================================
Configuration:
  - Max Iterations: 7
  - Success Threshold: 95.0%
  - Weights: {'clarity': 0.4, 'position': 0.3, 'size': 0.3}

============================================================
📸 NODE: Analyze Target Image
============================================================
  📝 Detected: '在你的桌面上不能使用手机' (confidence: 94.32%)

✅ Target Metrics Extracted:
  - Avg Confidence: 94.32%
  - Vertical Position: 66.7%
  - Estimated Font Size: 34px

============================================================
🎬 NODE: Generate Video (Iteration 1)
============================================================
  Font Size: 34px
  Stroke Width: 2px
  Position: 66.7%

============================================================
📸 NODE: Take Screenshot
============================================================
  ✅ Screenshot saved: iteration_1_screenshot.png

============================================================
🔍 NODE: Analyze Current Screenshot
============================================================
  📝 '在你的桌面上不能使用手机' (confidence: 95.12%)

============================================================
📊 NODE: Compare with Target
============================================================
  ✅ Clarity Score: 92.0/100
  ✅ Position Score: 98.5/100
  ✅ Size Score: 100.0/100
  🎯 Overall Score: 95.8/100
  ⭐ NEW BEST!

🎉 Success! Score 95.8 >= 95.0

============================================================
✅ RESOLVER: Graph Execution Complete
============================================================

💾 Results saved: output\iteration_results.json

============================================================
🏆 FINAL SUMMARY
============================================================
Total Iterations: 1
Stop Reason: Success! Score 95.8 >= 95.0

Best Result (Iteration 1):
  Overall Score: 95.8/100
  - Clarity: 92.0/100
  - Position: 98.5/100
  - Size: 100.0/100

Best Video: D:\video-agent\agent\output\10_second_1.mp4
============================================================
```

## **Key Features**

✅ **Graph-Based**: Clear node-edge-stop architecture  
✅ **Configurable**: All parameters adjustable  
✅ **Resolver**: Orchestrates until problem solved  
✅ **Smart Edges**: Conditional transitions based on scores  
✅ **Iterative**: Keeps trying until success or max reached  
✅ **Traceable**: Logs every node execution  

## **Configuration Options**

### **Max Iterations**
```python
max_iterations=7  # Default: try up to 7 times
```

### **Success Threshold**
```python
success_threshold=95.0  # Default: 95% match required
```

### **Comparison Weights**
```python
comparison_weights={
    'clarity': 0.4,   # OCR confidence weight
    'position': 0.3,  # Position match weight  
    'size': 0.3       # Font size match weight
}
# Must sum to 1.0
```

### **Parameter Ranges**
```python
font_size_range=[28, 30, 32, 34, 36, 38, 40]
stroke_width_range=[1, 2, 3]
position_range=[0.60, 0.63, 0.65, 0.67, 0.70]
```

## **Output Files**

```
agent/
├── output/
│   ├── 10_second_1.mp4           ← First iteration
│   ├── 10_second_2.mp4           ← Second iteration (if needed)
│   ├── ...
│   └── iteration_results.json    ← Complete results
│
└── screenshots/
    ├── iteration_1_screenshot.png
    ├── iteration_2_screenshot.png
    └── ...
```

## **Results JSON Structure**

```json
{
  "timestamp": "2025-10-16T07:30:00",
  "config": {
    "max_iterations": 7,
    "success_threshold": 95.0,
    "comparison_weights": {...}
  },
  "target_metrics": {...},
  "all_iterations": [...],
  "best_result": {
    "iteration": 1,
    "parameters": {...},
    "comparison": {...},
    "video_path": "..."
  },
  "stop_reason": "Success! Score 95.8 >= 95.0",
  "total_iterations": 1
}
```

## **Graph Concepts Explained**

### **Nodes**
- Self-contained processing units
- Each has clear input/output
- Can be reused and tested independently

### **Edges**  
- Conditional transitions between nodes
- Implement business logic (when to stop, when to continue)
- Keep graph flow clean and readable

### **Stop Conditions**
- Success: Score meets threshold
- Max Iterations: Tried enough times
- Error: Something went wrong

### **Resolver**
- Controls overall execution
- Manages state across nodes
- Enforces edge conditions
- Ensures problem gets solved (or reports why not)

---

**The graph executes until problem is solved or 7 iterations reached!** 🚀
