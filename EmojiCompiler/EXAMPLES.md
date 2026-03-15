# 🌈 Emoji Programming Language Showcase

Welcome to the **EmojiLang Compiler** documentation! This guide contains **20+ working examples** that you can copy and paste directly into the editor. These examples cover every symbol in the language, from basic math to complex logic.

---

## 🏗️ 1. The Core Structure (START/END)

Every program must begin with 🙂 and end with 🔚.

### Example 1: Absolute Minimum
```text
🙂
🔚
```

### Example 2: Minimal Print
```text
🙂
📢 1
🔚
```

---

## 🆕 2. Variable Declarations & Assignments

Use `🆕` only for the first time you create a variable. Use the name directly to update it.

### Example 3: Simple Declaration
```text
🙂
🆕 x = 10
📢 x
🔚
```

### Example 4: Variable Update (Assignment)
```text
🙂
🆕 count = 1
count = 5
📢 count
🔚
```

### Example 5: Variable to Variable
```text
🙂
🆕 a = 100
🆕 b = a
📢 b
🔚
```

---

## 📢 3. Printing (output)

### Example 6: Print Number
```text
🙂
📢 999
🔚
```

### Example 7: Print Multiple Times
```text
🙂
📢 1
📢 2
📢 3
🔚
```

---

## ➕ ➖ ✖ ➗ 4. Basic Math Operators

### Example 8: Addition
```text
🙂
🆕 sum = 10 ➕ 5
📢 sum
🔚
```

### Example 9: Subtraction
```text
🙂
🆕 diff = 20 ➖ 8
📢 diff
🔚
```

### Example 10: Multiplication
```text
🙂
🆕 prod = 4 ✖ 4
📢 prod
🔚
```

### Example 11: Division
```text
🙂
🆕 quot = 20 ➗ 5
📢 quot
🔚
```

### Example 12: Complex Expression
```text
🙂
🆕 result = 10 ➕ 5 ✖ 2 ➖ 4
📢 result
🔚
```

---

## ❓ 🔁 ➡ 5. Conditional Logic (IF/ELSE)

### Example 13: Simple IF
```text
🙂
🆕 age = 20
❓ age > 18 ➡
    📢 1
🔚
```

### Example 14: IF and ELSE
```text
🙂
🆕 score = 40
❓ score > 50 ➡
    📢 100
🔁
    📢 0
🔚
```

### Example 15: Nested IF (Multiple Logic)
```text
🙂
🆕 x = 10
❓ x == 10 ➡
    📢 x
🔚
```

---

## 🔄 ➡ 6. Loops (WHILE)

### Example 16: Basic Counter Loop
```text
🙂
🆕 i = 1
🔄 i < 4 ➡
    📢 i
    i = i ➕ 1
🔚
```

### Example 17: Countdown
```text
🙂
🆕 i = 5
🔄 i > 0 ➡
    📢 i
    i = i ➖ 1
🔚
```

---

## 🧩 7. Advanced & Combined Logic

### Example 18: Loop with IF Inside
```text
🙂
🆕 x = 1
🔄 x < 6 ➡
    ❓ x == 3 ➡
        📢 333
    🔁
        📢 x
    x = x ➕ 1
🔚
```

### Example 19: The "Bank Balance" Simulation
```text
🙂
🆕 balance = 100
🆕 withdrawal = 40
balance = balance ➖ withdrawal
❓ balance > 50 ➡
    📢 balance
🔁
    📢 0
🔚
```

### Example 20: Multiplication Table (Partial)
```text
🙂
🆕 n = 5
🆕 i = 1
🔄 i < 5 ➡
    📢 n ✖ i
    i = i ➕ 1
🔚
```

### Example 21: Final Boss (All Symbols)
```text
🙂
🆕 count = 1
🆕 max = 3
🔄 count == max ➡
    📢 0
🆕 a = 10
🆕 b = 2
❓ a ➗ b == 5 ➡
    📢 a ➕ b
🔚
```

---

## 🔡 8. String Support (Text)

You can now use double quotes to handle text!

### Example 22: Basic String
```text
🙂
🆕 message = "Hello World"
📢 message
🔚
```

### Example 23: String Assignment
```text
🙂
🆕 text = "Original"
text = "Updated Text"
📢 text
🔚
```

---

## 📜 Symbol Reference Cheat Sheet

| Symbol | Syntax | Meaning |
| :--- | :--- | :--- |
| 🙂 | `🙂` | Start of code |
| 🔚 | `🔚` | End of code |
| 🆕 | `🆕 var = val` | Variable declaration |
| 📢 | `📢 expr` | Print to console |
| ➕ | `a ➕ b` | Addition |
| ➖ | `a ➖ b` | Subtraction |
| ✖ | `a ✖ b` | Multiplication |
| ➗ | `a ➗ b` | Division |
| ❓ | `❓ cond ➡` | If-statement start |
| 🔁 | `🔁` | Else-statement start |
| 🔄 | `🔄 cond ➡` | While-loop start |
| ➡ | `... ➡` | Do/Then action |
