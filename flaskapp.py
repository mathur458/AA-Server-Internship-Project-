from main import create_app

flask_app = create_app()

for rule in flask_app.url_map.iter_rules():
    print(">>> ROUTE:", rule)

if __name__ == '__main__':
    flask_app.run(debug=True)
