# **AI Brain Development Guide**

This guide focuses on the implementation details of the AIbrain class. Your goal is to create a "driver" that takes sensor inputs and produces control outputs.

## **1\. File Location & Naming**

* **Location:** /AI\_engines/  
* **File Name:** AIbrain\_\<YourTeamName\>.py (e.g., AIbrain\_TurboDotNet.py)  
* **Class Name:** Must match the filename suffix (e.g., class AIbrain\_TurboDotNet:)

## **2\. The Interface (Contract)**

Your class functions like a service implementing an interface. It requires specific methods to be callable by the main game loop.

class AIbrain\_YourName:  
    def \_\_init\_\_(self):  
        \# Initialize your "DNA" (weights, biases) here  
        pass

    def decide(self, sensor\_data, time\_passed):  
        \# Core logic loop (Tick)  
        \# Input: sensor\_data (Raycast distances)  
        \# Output: Control signals  
        pass

### **Inputs: sensor\_data**

This is a list (or numpy array) of floats representing distances to obstacles.

* sensor\_data\[0\]: Front-Left ray  
* sensor\_data\[1\]: Front-Right ray  
* ...and so on.  
* **Tip:** Normalize these values (e.g., 1.0 \= immediate crash, 0.0 \= clear path) if you use a Neural Network.

### **Outputs: Control Signals**

The decide method must return an array/list of 4 integers (boolean logic):

1. **Forward (Gas):** 1 to accelerate, 0 to release.  
2. **Backward (Brake/Reverse):** 1 to brake/reverse.  
3. **Left:** 1 to steer left.  
4. **Right:** 1 to steer right.

## **3\. Development Workflow**

### **Phase A: The "Hello World" (Sanity Check)**

Before writing complex algorithms, ensure your class is hooked up correctly.

1. Create the file.  
2. Implement decide to simply return \[1, 0, 0, 0\] (Always Gas).  
3. Update main.py imports to point to your new file.  
4. **Result:** The car should drive straight into a wall. If it doesn't move, check your wiring.

### **Phase B: Rule-Based Logic (Hardcoded)**

Useful for understanding the sensors.  
Write if/else statements.

* *Example:* if sensor\_data\[left\_ray\_index\] \< 50: turn\_right()  
* **Why:** This helps you visualize what the sensors are actually "seeing" and confirms that sensor\_data is being passed correctly.

### **Phase C: The Evolutionary Approach (The Goal)**

In this project, you shouldn't hardcode rules (like above). You need to implement a **Linear Classifier** or a **Simple Neural Network**.

Concept:  
Instead of if (x \< 5), you compute:

$$Output \= Input \\cdot Weights \+ Bias$$

1. **Genotype (DNA):** Your class needs to store weights. In the beginning, these are random.  
2. **Phenotype (Behavior):** The decide method calculates outputs based on sensor\_data \* weights.  
3. **Mutation (Methods needed later):** You will likely need methods to export/import these weights (saving the brain) and a method to slightly randomize them (mutation) for the genetic algorithm in TrainingScene.

## **4\. Detailed Step-by-Step Workflow**

This workflow assumes you are building a **Linear Perceptron** (simple neural network without hidden layers), which is often sufficient for this task.

### **Step 1: Define the Architecture (Constructor)**

* **Inputs:** You have 5 sensors (rays) \+ 1 speed input (optional) \+ 1 Bias input (constant). Total \~6-7 inputs.  
* **Outputs:** You have 4 actions (Forward, Backward, Left, Right).  
* **Matrix:** You need a Weight Matrix of size \[Inputs x Outputs\] (e.g., 7x4).  
* **Action:** In \_\_init\_\_, initialize this matrix with random numbers between \-1.0 and 1.0.

### **Step 2: The Forward Pass (Decide Method)**

* **Normalize:** Convert raw sensor distance (e.g., 0 to 500 pixels) to a 0.0-1.0 range. Neural networks hate large numbers.  
  * normalized\_input \= raw\_input / max\_ray\_length  
* **Calculate:** Perform Matrix Multiplication.  
  * outputs \= np.dot(inputs, weights)  
* **Activation:** Decide the threshold.  
  * If output\[0\] \> 0 \-\> Gas ON.  
  * If output\[2\] \> output\[3\] \-\> Turn Left (or similar logic).

### **Step 3: Persistence (Save/Load)**

* Implement a method to save your weights to a .npz or .csv file.  
* **Why:** When you find a car that drives well in the simulation, you must save its "brain" immediately. If you restart the app, the RAM is cleared and your best racer is dead.

### **Step 4: Mutation (Evolution)**

* Implement a mutate(mutation\_rate) method.  
* **Logic:** Iterate through your weights. With a small probability (e.g., 5%), change the weight slightly (e.g., weight \+= random(-0.1, 0.1)).  
* **Context:** This method is called by the TrainingScene when creating the next generation of cars from the best parent.

## **5\. Tips, Tricks & Ideas**

### **1\. Data Normalization is Key**

In .NET/Business logic, 500 is just an integer. In AI, 500 is a massive number that will explode your gradients or calculations.

* **Rule:** Always squash inputs to 0.0 \- 1.0 or \-1.0 \- 1.0.  
* *Bad:* Input \= 450 (pixels)  
* *Good:* Input \= 0.9 (ratio)

### **2\. The "Bias" Neuron**

Linear algebra passes through the origin (0,0). If all sensors are 0 (no walls nearby), the output might be 0 (no gas).

* **Trick:** Always add a "fake" sensor input that is hardcoded to 1.0.  
* This allows the car to have a "default behavior" (e.g., drive forward) even when seeing nothing.

### **3\. Debugging with Visuals**

You cannot step-debug efficiently in real-time simulations.

* **Trick:** Use print() inside decide() sparingly.  
* **Better:** Observe behavior.  
  * *Car spins in circles?* \-\> One weight is too high, causing a permanent turn signal.  
  * *Car doesn't move?* \-\> Bias for "Gas" is negative.  
  * *Car jitters?* \-\> Inputs are conflicting rapidly.

### **4\. Fitness Function (Meta-Game)**

You don't code the fitness function (it's in the engine), but you need to understand it.

* Usually, Fitness \= Distance Traveled.  
* **Strategy:** Your car just needs to survive. Speed is secondary initially. Survival \= Distance.

### **5\. Start Simple\!**

Don't build a Deep Neural Network with TensorFlow/PyTorch yet.

* Start with a single matrix (Linear Regression).  
* Only add "Hidden Layers" (making it Deep) if the linear model fails to solve complex corners.

## **6\. .NET vs Python Cheatsheet**

| Concept | .NET / C\# | Python / Numpy |
| :---- | :---- | :---- |
| **Array** | float\[\] or List\<float\> | np.array(\[...\]) |
| **Matrix Mult** | Nested for loops | np.dot(A, B) |
| **Random** | new Random().NextDouble() | np.random.uniform(-1, 1\) |
| **Serialization** | JsonSerializer / XML | np.savez() / pickle |
| **Interfaces** | interface ICar { ... } | Duck typing (just implement methods) |

