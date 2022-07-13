from flask import Flask, render_template, request
#python -m venv ./venv
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    try: 
        if request.method == 'POST':
            import pip._vendor.requests as requests
            import json
            summonerName = request.form['summonerName']
            api_key = 'api_key=RGAPI-4b42ec90-adcf-44c4-bbfe-377c0d71f566'
            link = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?{api_key}'

            response = requests.get(link)
            id_data = json.loads(response.text)

            encrypted_id = str(id_data['id'])
            puuid = str(id_data['puuid'])

            link2 = f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{encrypted_id}?{api_key}'
            response2 = requests.get(link2)
            ranked_data = json.loads(response2.text)

            winrate = int((ranked_data[0]['wins'] / (ranked_data[0]['wins'] + ranked_data[0]['losses'])) * 100)

            output = (f"{summonerName: ^15}\n{ranked_data[0]['tier']} {ranked_data[0]['rank']} {ranked_data[0]['leaguePoints']} LP\n{winrate}% WR ({ranked_data[0]['wins']}W/{ranked_data[0]['losses']}L)")


            return render_template('index.html', value = output)

        else:
            return render_template('index.html')
    
    except IndexError as index_error:
        output = f"Error Retrieving Summoner\n... Try Again (viewer is case sensitive)"
        return render_template('index.html', value = output)

    except KeyError as key_error:
        output = f"Error Retrieving Summoner\n... Try Again (viewer is case sensitive)"
        return render_template('index.html', value = output)


@app.route('/owen')
def owen():
    return "hello"

if __name__ == '__main__':
    app.run(debug=True)