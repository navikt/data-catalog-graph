from flask import redirect
import connexion


# Create the application instance
app = connexion.App(__name__, specification_dir="./")

# Read the swagger.yml file to configure the endpoints
app.add_api("swagger.yml")

@app.route("/")
def swagger():
    return redirect('/api/ui')

if __name__ == "__main__":
    app.run(debug=True)