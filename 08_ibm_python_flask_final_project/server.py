'''
    Emotion detection application deployed on localhost:5000
'''
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Sentiment Analyzer")

@app.route("/emotionDetector")
def emot_detector():
    ''' Emotion detection of given text '''
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_analyze)

    anger = response['anger']
    disgust = response['disgust']
    fear = response['fear']
    joy = response['joy']
    sadness = response['sadness']
    dominant_emotion = response['dominant_emotion']

    if dominant_emotion is None:
        return " Invalid text! Please try again!"

    result_string = (
        "For the given statement, the system response is: " +
        "'anger': " + str(anger) + ", " +
        "'disgust': " + str(disgust) + ", " +
        "'fear': " + str(fear) + ", " +
        "'joy': " + str(joy) + " and " +
        "'sadness': " + str(sadness) + ". " +
        "The dominant emotion is " + str(dominant_emotion) + "."
    )

    return result_string

@app.route("/")
def render_index_page():
    ''' template index render '''
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000)
