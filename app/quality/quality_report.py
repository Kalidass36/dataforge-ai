class QualityReport:

    def __init__(self, profile):

        self.profile = profile

    def calculate_score(self):

        tables = len(
            self.profile["tables"]
        )

        null_issues = len(
            self.profile["null_issues"]
        )

        duplicate_issues = len(
            self.profile["duplicate_issues"]
        )

        anomaly_issues = sum(
            1
            for anomaly
            in self.profile["anomalies"]
            if anomaly.get(
                "anomaly_count",
                0
            ) > 0
        )

        if tables == 0:

            return 0

        penalty = (
            null_issues * 5
            + duplicate_issues * 5
            + anomaly_issues * 5
        )

        score = max(
            0,
            100 - penalty
        )

        return score

    def build(self):

        return {
            "quality_score":
                self.calculate_score(),

            "table_count":
                len(self.profile["tables"]),

            "null_issues":
                self.profile["null_issues"],

            "duplicate_issues":
                self.profile["duplicate_issues"],

            "anomalies":
                self.profile["anomalies"],
        }