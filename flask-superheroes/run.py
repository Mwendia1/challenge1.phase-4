from app import create_app

app = create_app()

print("Registered routes:")
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.rule}")

if __name__ == '__main__':
    app.run(port=5555, debug=True)