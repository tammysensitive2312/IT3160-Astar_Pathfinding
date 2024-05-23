import json

import convertJson as cj
import astar as algo
from flask import Flask, render_template, request

app = Flask(__name__)

# back-end flask api python
# fe sử dụng thư viện leaflets của js

""" lớp để tạo bản đồ osm sử dụng thư viện folium dưới dạng web sử dụng thư viện flask """


# api get để xử ly dữ liệu và tạo đường đi
@app.route('/calculate', methods=['GET'])
def control():
    # 4 giá trị [][]  [][]
    pntdata = request.args.get('pntdata')
    if pntdata is None:
        return json.dumps({'error': 'Missing parameter pntdata'}), 400  # Trả về lỗi 400 Bad Request
    raw_input = pntdata.split(',')

    input_source_loc = (float(raw_input[0]), float(raw_input[1]))
    input_dest_loc = (float(raw_input[2]), float(raw_input[3]))

    mapped_source_loc = cj.get_KNN(input_source_loc)
    mapped_dest_loc = cj.get_KNN(input_dest_loc)

    path = algo.aStar(mapped_source_loc, mapped_dest_loc)
    final_path, cost = cj.get_response_path_dict(path, mapped_source_loc, mapped_dest_loc)

    print("Cost of the path(km): " + str(cost))
    return json.dumps(final_path)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
