#Imports 
from datetime import datetime
from models import db
from models.user import User
from models.patientReward import PatientReward


#Reward Service Functions 

def get_claimed_rewards(username):

    user = User.query.filter_by(username=username).first()
    if not user or not user.patient:
        return {}

    rewards = PatientReward.query.filter_by(patient_id=user.patient.patient_id).all()
    
    #Return reward IDs as strings for consistency with frontend matching
    return {str(r.reward_id): r.claimed_at for r in rewards}


def mark_reward_claimed(username, reward_id, reward_name):

    reward_id = str(reward_id)  #Normalize to string for consistency

    user = User.query.filter_by(username=username).first()
    if not user or not user.patient:
        return False

    patient_id = user.patient.patient_id

    #Check if already claimed
    existing = PatientReward.query.filter_by(
        patient_id=patient_id,
        reward_id=reward_id
    ).first()

    if existing:
        return False  #Already claimed

    #Create and save new reward claim
    reward = PatientReward(
        patient_id=patient_id,
        reward_id=reward_id,
        reward_name=reward_name,
        claimed_at=datetime.utcnow()
    )
    db.session.add(reward)
    db.session.commit()

    return True
