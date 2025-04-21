#Imports
from datetime import datetime
from models import db
from models.patientGoal import PatientGoal
from models.user import User


#Goal Service Functions

def get_patient_goals(username):

    user = User.query.filter_by(username=username).first()
    if not user or not user.patient:
        return []
    
    return PatientGoal.query.filter_by(patient_id=user.patient.patient_id).all()


def set_patient_goal(username, metric_name, goal_value, goal_type="daily"):
  
    user = User.query.filter_by(username=username).first()
    if not user or not user.patient:
        return False

    patient_id = user.patient.patient_id

    #Check if a goal already exists for this metric and type
    existing_goal = PatientGoal.query.filter_by(
        patient_id=patient_id,
        metric_name=metric_name,
        goal_type=goal_type
    ).first()

    if existing_goal:
        #Update the existing goal
        existing_goal.goal_value = goal_value
        existing_goal.goal_type = goal_type
    else:
        #Create a new goal
        goal = PatientGoal(
            patient_id=patient_id,
            metric_name=metric_name,
            goal_value=goal_value,
            goal_type=goal_type,
        )
        db.session.add(goal)

    db.session.commit()
    return True


def delete_patient_goal(goal_id):

    goal = PatientGoal.query.get(goal_id)
    if goal:
        db.session.delete(goal)
        db.session.commit()
        return True

    return False
