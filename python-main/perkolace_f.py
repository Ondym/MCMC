from collections import deque


def perk(array):
    if not array or not array[0]:  # Check for empty array or empty row
        return 0

    rows, cols = len(array), len(array[0])

    if rows == 0 or cols == 0:
        return 0

    # Initialize the queue with all '1's in the first row
    queue = deque([(0, c) for c in range(cols) if array[0][c] == 1])
    visited = set((0, c) for c in range(cols) if array[0][c] == 1)

    while queue:
        x, y = queue.popleft()

        # If we reach any cell in the last row, return True
        if x == rows - 1:
            return 1

        # Explore the neighbors (up, down, left, right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and array[nx][ny] == 1 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))

    return 0



