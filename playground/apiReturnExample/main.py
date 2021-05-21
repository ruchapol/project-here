@app.route('/road_jf')
def road_jf():
    predict = request.args.get('predict', default = 1, type = int)
    road_code = [("219+00638", 22021), ("219-02600", 46771),
                 ("219+00661", 35518), ("219-00567", 41007),
                 ("219-02427", 46335), ("219+00640", 22025),
                 ("219+00639", 22032), ("219+00639", 22022),
                 ("219+00639", 22023), ("219+00639", 22024),
                 ("219+00639", 22033)]

    jf_res = {}

    for road_li, road_pc in road_code:
        pop = random.random()
        if (pop < .7):
            jf = random.uniform(1, 10)
        else:
            jf = 10.0
        if (jf < 4 ): jf_color = "Green"
        if (jf >= 4 and jf < 8): jf_color = "Yellow"
        if (jf >= 8 and jf < 10): jf_color = "Red"
        if (jf >= 10.0):jf_color = "Black"

        jf_str = "%.3f" % (jf, )
        try:
            jf_res[road_li][road_pc] = [jf_str, jf_color]
        except KeyError:
            jf_res[road_li] = {road_pc:[jf_str, jf_color]}
        # jf_res["%s,%s" % (road_li, road_pc)] = [jf_str, jf_color]

    return jsonify(jf_res)

# second unit
@app.route('/traval_time')
def travel_time():
    destination = request.args.get('des', default = "Wongsawang", type = str)
    predict = request.args.get('predict', default = 1, type = int)
    calulated_time = random.randrange(5, 100, 1)
    return json.dumps({"destination": destination, "time": calulated_time})