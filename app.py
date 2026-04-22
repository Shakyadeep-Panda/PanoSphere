import os
import json
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
app.config['TOURS_FOLDER']  = os.path.join(BASE_DIR, 'tours')
ALLOWED = {'jpg', 'jpeg', 'png', 'webp', 'gif'}


# -----------------------------
# Helpers
# -----------------------------
def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED


def safe_tour_name(name):
    safe_name = "".join(c for c in name if c.isalnum() or c in ('-', '_')).strip()
    return safe_name if safe_name else "default"


def get_tour_file(name):
    return os.path.join(app.config['TOURS_FOLDER'], f"{safe_tour_name(name)}.json")


def ensure_dirs():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['TOURS_FOLDER'], exist_ok=True)


def default_tour(name="default"):
    return {
        'nodes': {},
        'matrix': {},
        'name': safe_tour_name(name)
    }


def load_tour(name="default"):
    ensure_dirs()
    file_path = get_tour_file(name)

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    return default_tour(name)
                data.setdefault('nodes', {})
                data.setdefault('matrix', {})
                data.setdefault('name', safe_tour_name(name))
                return data
        except Exception:
            return default_tour(name)

    return default_tour(name)


def save_tour(data, name="default"):
    ensure_dirs()
    file_path = get_tour_file(name)

    if not isinstance(data, dict):
        data = default_tour(name)

    data.setdefault('nodes', {})
    data.setdefault('matrix', {})
    data['name'] = safe_tour_name(name)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def list_tours():
    ensure_dirs()
    tours = []

    for file in os.listdir(app.config['TOURS_FOLDER']):
        if file.endswith('.json'):
            tours.append(file[:-5])

    if 'default' not in tours:
        save_tour(default_tour("default"), "default")
        tours.append('default')

    return sorted(set(tours))


# -----------------------------
# Routes
# -----------------------------
@app.route('/favicon.ico')
def favicon():
    return '', 204


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/tours', methods=['GET'])
def get_tours():
    return jsonify({'tours': list_tours()})


@app.route('/api/tour/<tour_name>', methods=['GET'])
def get_tour_api(tour_name):
    return jsonify(load_tour(tour_name))


@app.route('/api/tour/<tour_name>', methods=['POST'])
def save_tour_api(tour_name):
    existing = load_tour(tour_name)
    incoming = request.get_json(silent=True) or {}

    if not isinstance(incoming, dict):
        incoming = {}

    existing.update(incoming)
    save_tour(existing, tour_name)
    return jsonify({'ok': True, 'tour': existing})


@app.route('/api/tour/<tour_name>', methods=['DELETE'])
def delete_tour_api(tour_name):
    tour_name = safe_tour_name(tour_name)

    if tour_name == 'default':
        return jsonify({'error': 'Default tour cannot be deleted'}), 400

    file_path = get_tour_file(tour_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'ok': True})

    return jsonify({'error': 'Tour not found'}), 404


@app.route('/api/upload/<tour_name>', methods=['POST'])
def upload(tour_name):
    ensure_dirs()

    if 'files' not in request.files:
        return jsonify({'error': 'No files'}), 400

    files = request.files.getlist('files')
    uploaded = []
    tour = load_tour(tour_name)

    for file in files:
        if file and file.filename and allowed(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            node_id = str(uuid.uuid4())[:8]
            filename = f"{node_id}.{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(filepath)

            node = {
                'id': node_id,
                'name': os.path.splitext(file.filename)[0],
                'filename': filename,
                'links': []
            }

            tour['nodes'][node_id] = node
            uploaded.append(node)

    save_tour(tour, tour_name)
    return jsonify({'uploaded': uploaded})


@app.route('/api/nodes/<tour_name>/<node_id>', methods=['PUT'])
def update_node(tour_name, node_id):
    tour = load_tour(tour_name)

    if node_id not in tour['nodes']:
        return jsonify({'error': 'Not found'}), 404

    incoming = request.get_json(silent=True) or {}
    if not isinstance(incoming, dict):
        incoming = {}

    tour['nodes'][node_id].update(incoming)
    save_tour(tour, tour_name)

    return jsonify(tour['nodes'][node_id])


@app.route('/api/nodes/<tour_name>/<node_id>', methods=['DELETE'])
def delete_node(tour_name, node_id):
    tour = load_tour(tour_name)

    if node_id in tour['nodes']:
        fname = tour['nodes'][node_id].get('filename')
        if fname:
            fp = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            if os.path.exists(fp):
                os.remove(fp)

        del tour['nodes'][node_id]

        # Remove from matrix
        tour['matrix'] = {k: v for k, v in tour.get('matrix', {}).items() if v != node_id}

        # Remove links pointing to deleted node
        for n in tour['nodes'].values():
            n['links'] = [l for l in n.get('links', []) if l.get('nodeId') != node_id]

        save_tour(tour, tour_name)

    return jsonify({'ok': True})


@app.route('/api/matrix/<tour_name>', methods=['POST'])
def save_matrix(tour_name):
    tour = load_tour(tour_name)
    incoming = request.get_json(silent=True) or {}
    matrix = incoming.get('matrix', {})

    if not isinstance(matrix, dict):
        matrix = {}

    tour['matrix'] = matrix
    nodes = tour['nodes']
    pos = {}

    for key, nid in matrix.items():
        if nid and nid in nodes:
            try:
                r, c = map(int, key.split(','))
                pos[nid] = (r, c)
            except:
                continue

    dirs = {'north': (-1, 0), 'south': (1, 0), 'east': (0, 1), 'west': (0, -1)}
    yaws = {'north': '0deg', 'south': '180deg', 'east': '90deg', 'west': '-90deg'}

    for nid, (r, c) in pos.items():
        auto = []

        for d, (dr, dc) in dirs.items():
            nk = f'{r+dr},{c+dc}'
            nb = matrix.get(nk)

            if nb and nb in nodes:
                auto.append({
                    'nodeId': nb,
                    'position': {'yaw': yaws[d], 'pitch': '-10deg'},
                    'name': nodes[nb]['name'],
                    'auto': True
                })

        existing = [l for l in nodes[nid].get('links', []) if not l.get('auto')]
        nodes[nid]['links'] = existing + auto

    save_tour(tour, tour_name)
    return jsonify({'ok': True, 'tour': tour})


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# -----------------------------
# Start
# -----------------------------
if __name__ == '__main__':
    ensure_dirs()
    list_tours()  # ensures default exists

    print(f"\n  Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"  Tours folder: {app.config['TOURS_FOLDER']}")
    print(f"  Open: http://localhost:5000\n")

    app.run(debug=True, port=5000, use_reloader=False)
