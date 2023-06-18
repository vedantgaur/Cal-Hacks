def Expression2Text(hume_output, model):
    emotion_ranges = [
        (0.26, 0.35),
        (0.35, 0.44),
        (0.44, 0.53),
        (0.53, 0.62),
        (0.62, 0.71),
        (0.71, 10),
    ]
    adverbs = ["slight", "some", "moderate", "quite some", "a lot of", "extreme"]


    if all(emotion[1] < emotion_ranges[0][0] for emotion in hume_output[model]):
        expression_text = "neutral"
    else:
        phrases = []
        for emotion in hume_output[model]:
            i = 0
            while not (emotion[1] < emotion_ranges[i][1] and emotion[1] > emotion_ranges[i][0]):
                i += 1
            phrases.append(f"{adverbs[i]} {emotion[0].lower()}")
        expression_text = ", ".join(phrases)

    return expression_text

def get_prompt(hume_output, code=""):
    return (
        f"""
        The interviewee's voice indicates the following emotions: {Expression2Text(hume_output, "language")}
        The interviewee's facial expression indicate the following emotions: {Expression2Text(hume_output, "face")}
        The interviewee's prosody indicates the following emotions: {Expression2Text(hume_output, "prosody")}
        The interviewee's vocal utterances indicate the following emotions: {Expression2Text(hume_output, "burst")}
        
        If the emotions indicated by a certain metric (voice, facial expression, prosody, or vocal utterances) disagree with the emotions indicated by the majority of metrics, weigh the emotions indicated by the majority of metrics more heavily.

        The interviewee says: {hume_output["transcript"] + code}
        """
    )