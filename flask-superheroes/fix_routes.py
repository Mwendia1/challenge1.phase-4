# fix_routes.py
import os
import sys

def update_file(file_path, old_content, new_content):
    with open(file_path, 'r') as f:
        content = f.read()
    
    if old_content in content:
        content = content.replace(old_content, new_content)
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Updated {file_path}")
        return True
    return False

# Update heroes.py
update_file(
    'app/routes/heroes.py',
    "heroes_bp = Blueprint('heroes', __name__)",
    "heroes_bp = Blueprint('heroes', __name__, url_prefix='/')"
)

# Update powers.py
update_file(
    'app/routes/powers.py',
    "powers_bp = Blueprint('powers', __name__)",
    "powers_bp = Blueprint('powers', __name__, url_prefix='/')"
)

#hero_powers.py
update_file(
    'app/routes/hero_powers.py',
    "hero_powers_bp = Blueprint('hero_powers', __name__)",
    "hero_powers_bp = Blueprint('hero_powers', __name__, url_prefix='/')"
)

print("Route fixes applied!")