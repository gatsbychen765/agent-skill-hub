#!/usr/bin/env python3
"""口算批改脚本 - 文本批量批改示例"""

import re
import sys

def evaluate(expr):
    """安全计算一道口算题"""
    expr = expr.replace('×', '*').replace('÷', '/')
    try:
        return eval(expr)
    except:
        return None

def grade(text):
    """批改文本形式的口算题"""
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    results = []
    correct = 0

    for i, line in enumerate(lines, 1):
        m = re.match(r'(.+?)=(.+)', line)
        if not m:
            results.append((i, line, '-', '-', '格式错误'))
            continue

        expr, answer = m.group(1), m.group(2).strip()
        expected = evaluate(expr)

        if expected is None:
            results.append((i, line, answer, '-', '无法计算'))
        elif abs(float(answer) - expected) < 0.001:
            results.append((i, line, answer, str(int(expected) if expected.is_integer() else expected), '✓'))
            correct += 1
        else:
            results.append((i, line, answer, str(int(expected) if expected.is_integer() else expected), '✗'))

    total = len(lines)
    accuracy = correct / total * 100 if total else 0

    print(f"\n{'='*40}")
    print(f"共 {total} 题，正确 {correct} 题")
    print(f"正确率：{accuracy:.0f}%，得分：{int(accuracy)} 分")
    print(f"{'='*40}\n")

    for i, line, ans, exp, mark in results:
        print(f"  {i:2d}. {line:15s} → {mark}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    grade(text)
