from models import db

class PatientChallenge(db.Model):
    __tablename__ = "patient_challenge"
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    progress = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)

    patient = db.relationship("Patient", back_populates="challenges")
    challenge = db.relationship("Challenge", back_populates="participants")

    def update_progress(self, amount):
        """Update the progress of the challenge."""
        if not self.completed:
            self.progress += amount
            if self.progress >= self.challenge.goal:
                self.progress = self.challenge.goal
                self.completed = True
                self.patient.reward_points += self.challenge.reward_points
            db.session.commit()
