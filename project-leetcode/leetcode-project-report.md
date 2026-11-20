# Project Leetcode

## Problem 1 [25 points]

### Problem Information

Problem Name: *1137. N-th Tribonacci Number*
The Tribonacci sequence Tn is defined as follows:
T0 = 0, T1 = 1, T2 = 1, and Tn+3 = Tn + Tn+1 + Tn+2 for n >= 0.
Given n, return the value of Tn.

[Submission Link](https://leetcode.com/problems/n-th-tribonacci-number/submissions/2195073857/)

![Screenshot 2026-11-12 at 22-54-57 N-th Tribonacci Number - LeetCode.png](Screenshot%202026-11-12%20at%2022-54-57%20N-th%20Tribonacci%20Number%20-%20LeetCode.png)
### Time Complexity

```python
class Solution:
    def tribonacci(self, n: int) -> int:
        T = [0, 1, 1]
        for i in range(3, n+1):                 # O(n) loop: runs n - 2 times
            T.append(T[i-1] + T[i-2] + T[i-3])  # O(1) per iteration
        return T[n]
```

*O(n)* because the loop executes n - 2 times, performing constant-time additions and list appends on each iteration.



### Space Complexity

```python
class Solution:
    def tribonacci(self, n: int) -> int:
        T = [0, 1, 1]                           # Initial base memory
        for i in range(3, n+1):
            T.append(T[i-1] + T[i-2] + T[i-3])  # List expands to store n + 1 elements
        return T[n]
```

*O(n)* because the list T grows linearly to store n + 1 elements of the sequence.

----

## Problem 2 [25 points]

### Problem Information

Problem Name: *Two Sum*

You are given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

[Submission Link](https://leetcode.com/problems/two-sum/submissions/2195073414/)

![Screenshot 2026-11-12 at 22-54-50 Two Sum - LeetCode.png](Screenshot%202026-11-12%20at%2022-54-50%20Two%20Sum%20-%20LeetCode.png)
### Time Complexity

```python
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        numMap = {}
        for i, num in enumerate(nums):          # O(n) loop: iterates through the list once
            complement = target - num
            if complement in numMap:            # O(1) average lookup in hash map
                return [numMap[complement], i]
            numMap[num] = i                     # O(1) insertion in hash map
```

*O(n)* because the loop iterates through the list of length $n$ once, performing O(1) hash map lookups and insertions.
### Space Complexity

```python
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        numMap = {}                             # Hash map stores up to n elements
        for i, num in enumerate(nums):
            complement = target - num
            if complement in numMap:
                return [numMap[complement], i]
            numMap[num] = i                     # Stores numbers and indices
```

*O(n)* because the dictionary numMap stores up to n elements in the worst-case scenario.
----

## Problem 3 [25 points]

### Problem Information

Problem Name: *Combination Sum*

Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.

The test cases are generated such that the number of unique combinations that sum up to target is less than 150 combinations for the given input.

[Submission Link](https://leetcode.com/problems/combination-sum/submissions/2195043242/)

![Screenshot 2026-11-12 at 22-54-42 Combination Sum - LeetCode.png](Screenshot%202026-11-12%20at%2022-54-42%20Combination%20Sum%20-%20LeetCode.png)

### Time Complexity

```python
class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        result = []

        def backtrack(start, current, total):
            if total == target:
                result.append(current.copy())
                return

            for i in range(start, len(candidates)):          # Explores possible combinations recursively
                num = candidates[i]
                if total + num > target:
                    continue
                current.append(num)
                backtrack(i, current, total + num)           # Exponential time based on target and minimum candidate
                current.pop()

        backtrack(0, [], 0)
        return result
```

*O(2/(Target/Min))*, because the backtracking tree branches out depending on the target value and the smallest candidate size.

### Space Complexity

```python
class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:
        result = []

        def backtrack(start, current, total):
            if total == target:
                result.append(current.copy())
                return

            for i in range(start, len(candidates)):
                num = candidates[i]
                if total + num > target:
                    continue
                current.append(num)
                backtrack(i, current, total + num)           # Recursion stack depth proportional to target / min candidate
                current.pop()

        backtrack(0, [], 0)
        return result                                        # Stores all valid combinations
```

*O(2/(Target/Min))*, for the maximum recursion stack depth (excluding the memory required to store the final output results).

----

## Problem 4 [10 points]

### Problem Information

Problem Name: *Queue Reconstruction by Height*

You are given an array of people, people, which are the attributes of some people in a queue (not necessarily in order). Each people[i] = [hi, ki] represents the ith person of height hi with exactly ki other people in front who have a height greater than or equal to hi.

Reconstruct and return the queue that is represented by the input array people. The returned queue should be formatted as an array queue, where queue[j] = [hj, kj] is the attributes of the jth person in the queue (queue[0] is the person at the front of the queue).

[Submission Link](https://leetcode.com/problems/queue-reconstruction-by-height/submissions/2195047940/)

![Screenshot 2026-11-12 at 22-54-33 Queue Reconstruction by Height - LeetCode.png](Screenshot%202026-11-12%20at%2022-54-33%20Queue%20Reconstruction%20by%20Height%20-%20LeetCode.png)

### Time Complexity

```python
class Solution:
    def reconstructQueue(self, people: list[list[int]]) -> list[list[int]]:
        def sort_key(person):
            return (-person[0], person[1])

        people.sort(key=sort_key)                       # O(n log n) for sorting

        queue = []

        for person in people:
            queue.insert(person[1], person)             # O(n) per insertion due to element shifting

        return queue
```

*O(n^2)* because inserting elements into a list takes O(n) time inside a loop that runs n times.

### Space Complexity

```python
class Solution:
    def reconstructQueue(self, people: list[list[int]]) -> list[list[int]]:
        def sort_key(person):
            return (-person[0], person[1])

        people.sort(key=sort_key)

        queue = []                                      # Stores all n elements in the result queue

        for person in people:
            queue.insert(person[1], person)

        return queue
```

*O(n)*  because the queue list stores alln elements in memory.

----

## Problem 5 [10 points]

### Problem Information

Problem Name: *Binary Tree Level Order Traversal*

Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

[Submission Link](https://leetcode.com/problems/binary-tree-level-order-traversal/submissions/2195054773/)

![Screenshot 2026-11-12 at 22-54-25 Binary Tree Level Order Traversal - LeetCode.png](Screenshot%202026-11-12%20at%2022-54-25%20Binary%20Tree%20Level%20Order%20Traversal%20-%20LeetCode.png)

### Time Complexity

```python
class Solution:
    def levelOrder(self, root):
        if not root:
            return []

        result = []
        queue = [root]
        index = 0

        while index < len(queue):               # O(n) loop: visits every node exactly once
            level = []
            level_size = len(queue)

            while index < level_size:
                node = queue[index]
                index += 1
                level.append(node.val)
                if node.left:
                    queue.append(node.left)     # O(1)
                if node.right:
                    queue.append(node.right)

            result.append(level)

        return result
```
O(n), because every node in the binary tree is visited and processed exactly once.

### Space Complexity

```python
class Solution:
    def levelOrder(self, root):
        if not root:
            return []

        result = []
        queue = [root]                      
        index = 0

        while index < len(queue):
            level = []
            level_size = len(queue)

            while index < level_size:
                node = queue[index]
                index += 1
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level)                # Stores all n node values in the output result

        return result
```
*O(n)* because the queue and result list store all n nodes,

----

## Problem 6 [5 points]

### Problem Information

Problem Name: *Min Cost to Connect All Points*

[Submission Link](https://leetcode.com/problems/min-cost-to-connect-all-points/)

![Screenshot 2026-11-12 at 22-54-10 Min Cost to Connect All Points - LeetCode.png](Screenshot%202026-11-12%20at%2022-54-10%20Min%20Cost%20to%20Connect%20All%20Points%20-%20LeetCode.png)

### Time Complexity

```python
class Solution:
    def minCostConnectPoints(self, points):
        n = len(points)
        min_cost = [float('inf')] * n
        visited = [False] * n
        min_cost[0] = 0
        total_cost = 0

        for _ in range(n):                              # O(n) outer loop
            current = -1
            for i in range(n):                          # O(n) inner loop
                if not visited[i]:
                    if current == -1 or min_cost[i] < min_cost[current]:
                        current = i
            visited[current] = True
            total_cost += min_cost[current]
            
            for i in range(n):                          # O(n) inner loop
                if not visited[i]:
                    distance = (
                        abs(points[current][0] - points[i][0]) +
                        abs(points[current][1] - points[i][1])
                    )
                    min_cost[i] = min(min_cost[i], distance)

        return total_cost
```
*O(n^2)*, because the outer loop runs $n$ times, and inside it, two separate loops iterate n times.

### Space Complexity

```python
class Solution:
    def minCostConnectPoints(self, points):
        n = len(points)
        min_cost = [float('inf')] * n                   # O(n) space
        visited = [False] * n                           # O(n) space
        min_cost[0] = 0
        total_cost = 0

        for _ in range(n):
            current = -1
            for i in range(n):
                if not visited[i]:
                    if current == -1 or min_cost[i] < min_cost[current]:
                        current = i
            visited[current] = True
            total_cost += min_cost[current]
            
            for i in range(n):
                if not visited[i]:
                    distance = (
                        abs(points[current][0] - points[i][0]) +
                        abs(points[current][1] - points[i][1])
                    )
                    min_cost[i] = min(min_cost[i], distance)

        return total_cost
```
*O(n)*, Both arrays require space equal to the number of points n

----

## Problem 7 [5 extra credit points]

### Problem Information

Problem Name: *Number of Provinces*

There are n cities. Some of them are connected, while some are not. If city a is connected directly with city b, and city b is connected directly with city c, then city a is connected indirectly with city c.

A province is a group of directly or indirectly connected cities and no other cities outside of the group.

You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.

[Submission Link](https://leetcode.com/problems/number-of-provinces/submissions/2195056804/)

![Screenshot 2026-11-12 at 22-53-35 Number of Provinces - LeetCode.png](Screenshot%202026-11-12%20at%2022-53-35%20Number%20of%20Provinces%20-%20LeetCode.png)

### Time Complexity

```python
class Solution:
    def findCircleNum(self, isConnected):
        n = len(isConnected)
        visited = set()
        provinces = 0

        def dfs(city):
            visited.add(city)
            for neighbor in range(n):                   # O(n): checks all neighbors
                if isConnected[city][neighbor] == 1 and neighbor not in visited:
                    dfs(neighbor)

        for city in range(n):                           # O(n): iterates through each city
            if city not in visited:
                provinces += 1
                dfs(city)                              

        return provinces
```

*O(n^2)*, because we visit every node in a nxn matrix

### Space Complexity

```python
class Solution:
    def findCircleNum(self, isConnected):
        n = len(isConnected)
        visited = set()                                 # O(n)
        provinces = 0

        def dfs(city):
            visited.add(city)
            for neighbor in range(n):
                if isConnected[city][neighbor] == 1 and neighbor not in visited:
                    dfs(neighbor)                       # O(n) worst-case recursion

        for city in range(n):
            if city not in visited:
                provinces += 1
                dfs(city)

        return provinces
```

*O(n)* because visited and recursion call both require n in the worst case.
----

## Problem 8 [5 extra credit points]

### Problem Information

Problem Name: *Lowest Common Ancestor of a Binary Tree*

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”

[Submission Link](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/submissions/2195058163/)

![Screenshot 2026-11-12 at 22-52-37 Lowest Common Ancestor of a Binary Tree - LeetCode.png](Screenshot%202026-11-12%20at%2022-52-37%20Lowest%20Common%20Ancestor%20of%20a%20Binary%20Tree%20-%20LeetCode.png)

### Time Complexity

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':

        if root is None or root == p or root == q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)    # O(n) visits every node in the tree
        right = self.lowestCommonAncestor(root.right, p, q)

        if left and right:
            return root

        return left if left else right
```
O(n)* because depth-first search visits every node in the worst case.

### Space Complexity

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':

        if root is None or root == p or root == q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)  # up to O(n) for a skewed tree

        if left and right:
            return root

        return left if left else right
```

*O(n)* in the worst case of the call stack reaching the height of the tree.
----

## Problem 9 [5 extra credit points]

### Problem Information

Problem Name: *Triangle*

Given a triangle array, return the minimum path sum from top to bottom.

For each step, you may move to an adjacent number of the row below. More formally, if you are on index i on the current row, you may move to either index i or index i + 1 on the next row.

[Submission Link](https://leetcode.com/problems/triangle/submissions/2195060343/)

![Screenshot 2026-11-12 at 22-52-29 Triangle - LeetCode.png](Screenshot%202026-11-12%20at%2022-52-29%20Triangle%20-%20LeetCode.png)

### Time Complexity

```python

class Solution:
    def minimumTotal(self, triangle):
        memo = {}

        def dfs(i, j):
            if i == len(triangle) - 1:
                return triangle[i][j]

            if (i, j) in memo:
                return memo[(i, j)]                     # O(1)

            left = dfs(i + 1, j)
            right = dfs(i + 1, j + 1)                   # O(1)

            memo[(i, j)] = triangle[i][j] + min(left, right)

            return memo[(i, j)]

        return dfs(0, 0)
```

 *O(n^2)* because memoization ensures each of the elements in the triangle are visited.

### Space Complexity

```python
class Solution:
    def minimumTotal(self, triangle):
        memo = {}                                       # O(n^2) for all triangle positions

        def dfs(i, j):
            if i == len(triangle) - 1:
                return triangle[i][j]

            if (i, j) in memo:
                return memo[(i, j)]

            left = dfs(i + 1, j)                        # O(n) maximum recursion stack depth
            right = dfs(i + 1, j + 1)

            memo[(i, j)] = triangle[i][j] + min(left, right)

            return memo[(i, j)]

        return dfs(0, 0)
```

*O(n^2)* because the memo dictionary stores a result for every element in the triangle, 

----

## Problem 10 [5 extra credit points]

### Problem Information

Problem Name: *Perfect Squares*

Given an integer n, return the least number of perfect square numbers that sum to n.

A perfect square is an integer that is the square of an integer; in other words, it is the product of some integer with itself. For example, 1, 4, 9, and 16 are perfect squares while 3 and 11 are not.

[Submission Link](https://leetcode.com/problems/perfect-squares/submissions/2195062624/)

![Screenshot 2026-11-12 at 22-52-21 Perfect Squares - LeetCode.png](Screenshot%202026-11-12%20at%2022-52-21%20Perfect%20Squares%20-%20LeetCode.png)

### Time Complexity

```python
class Solution:
    def numSquares(self, n: int) -> int:

        dp = [float('inf')] * (n + 1)
        dp[0] = 0

        for i in range(1, n + 1):                       # O(n)

            j = 1
            while j * j <= i:                           # O(sqrt(i))
                square = j * j
                dp[i] = min(
                    dp[i],
                    dp[i - square] + 1
                )
                j += 1

        return dp[n]
```

*O(n \sqrt{n})* because the outer loop runs n times, and the inner loop runs \sqrt{i} times for each number.

### Space Complexity

```python
class Solution:
    def numSquares(self, n: int) -> int:

        dp = [float('inf')] * (n + 1)                   # O(n) 
        dp[0] = 0

        for i in range(1, n + 1):
            j = 1
            while j * j <= i:
                square = j * j
                dp[i] = min(
                    dp[i],
                    dp[i - square] + 1
                )
                j += 1

        return dp[n]
```

*O(n)* because the dp array requires memory proportional to n + 1

## Project Review

*Fill me in*

---

## Problem 11 [5 extra credit points]

### Problem Information

Problem Name: *Flower Planting With No Adjacent*

You have n gardens, labeled from 1 to n, and an array paths where paths[i] = [xi, yi] describes a bidirectional path between garden xi to garden yi. In each garden, you want to plant one of 4 types of flowers.

All gardens have at most 3 paths coming into or leaving it.

Your task is to choose a flower type for each garden such that, for any two gardens connected by a path, they have different types of flowers.

Return any such a choice as an array answer, where answer[i] is the type of flower planted in the (i+1)th garden. The flower types are denoted 1, 2, 3, or 4. It is guaranteed an answer exists.

[Submission Link](https://leetcode.com/problems/flower-planting-with-no-adjacent/submissions/2195072715/)

![Screenshot 2026-11-12 at 22-52-14 Flower Planting With No Adjacent - LeetCode.png](Screenshot%202026-11-12%20at%2022-52-14%20Flower%20Planting%20With%20No%20Adjacent%20-%20LeetCode.png)

### Time Complexity

*Fill me in*

### Space Complexity

*Fill me in*

----

## Problem 12 [5 extra credit points]

### Problem Information

Problem Name: *Course Schedule*

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

Return true if you can finish all courses. Otherwise, return false.

[Submission Link](https://leetcode.com/problems/course-schedule/submissions/2195074775/)

![Screenshot 2026-11-12 at 22-52-02 Course Schedule - LeetCode.png](Screenshot%202026-11-12%20at%2022-52-02%20Course%20Schedule%20-%20LeetCode.png)

### Time Complexity

*Fill me in*

### Space Complexity

*Fill me in*

## Project Review

Owen did same as mine but without saving historic data in the array 
Owen did the same as I but his typing was better
Owen used dynapic programming.
Owen built a custom sorting program using relative position to improve efficiency.
He skipped to Binary tree reversal we both did basicaly the same as I did.
He also skipped to Number of provences and had a similar solution to me other than some basic differences in format.