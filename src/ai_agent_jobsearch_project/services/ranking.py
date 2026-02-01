
#Räkna ut värde för prognoser avseende framtida möjligheter till arbete
#Hämtas från Yrkesbarometern och översätts till int för att kunna beräkna prognos

JOB_SCORE = {
    "små": 1,
    "medelstora": 2,
    "stora": 3,
}

REK_SCORE = {
    "överskott": 0,
    "balans": 1,
    "paradox": 1,
    "brist": 2,
}

PROGNOS_SCORE = {
    "öka": 1,
    "vara oförändrad": 0,
    "minska": -1,
}

def apply_ranking(df):
    df = df.copy()

    df["job_score"] = df["jobbmojligheter"].map(JOB_SCORE).fillna(0)
    df["rek_score"] = df["rekryteringssituation"].map(REK_SCORE).fillna(0)
    df["prog_score"] = df["prognos"].map(PROGNOS_SCORE).fillna(0)

    df["rank_score"] = (
        df["job_score"] *10
        + df["rek_score"] * 2
        + df["prog_score"]
    )

    return df