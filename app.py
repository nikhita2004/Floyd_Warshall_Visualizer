from flask import Flask, render_template, request
import math

app = Flask(__name__)

def floyd_warshall(matrix):
    n = len(matrix)
    dist = [[matrix[i][j] for j in range(n)] for i in range(n)]
    steps = []
    explanations = []
    changed_cells_per_step = []

    for k in range(n):
        updated_cells = []
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    updated_cells.append((i, j))

        snapshot = [[("INF" if x == math.inf else x) for x in row] for row in dist]
        steps.append(snapshot)
        changed_cells_per_step.append(updated_cells)

        if updated_cells:
            cells = ", ".join([f"({i+1},{j+1})" for i, j in updated_cells])
            explanations.append(f"Step {k+1}: Updated cells {cells} using node {k+1} as intermediate.")
        else:
            explanations.append(f"Step {k+1}: No distances changed using node {k+1}.")

    final = [[("INF" if x == math.inf else x) for x in row] for row in dist]
    return steps, final, explanations, changed_cells_per_step

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    steps = result = explanations = changed_cells_per_step = None

    size = 3
    matrix = []

    if request.method == "POST":
        try:
            size = int(request.form.get("size", 3))
            matrix = []
            for i in range(size):
                row = []
                for j in range(size):
                    val = request.form.get(f"cell_{i}_{j}", "")
                    if val.strip().upper() == "INF" or val.strip() == "":
                        row.append(math.inf)
                    else:
                        row.append(int(val))
                matrix.append(row)

            steps, result, explanations, changed_cells_per_step = floyd_warshall(matrix)

        except Exception as e:
            error = str(e)

    if not matrix:
        matrix = [[0 if i==j else "INF" for j in range(size)] for i in range(size)]

    return render_template(
        "index.html",
        size=size,
        matrix=matrix,
        steps=steps,
        result=result,
        explanations=explanations,
        changed_cells_per_step=changed_cells_per_step,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
