from rest_framework import serializers
from .models import Functions, FunctionsGoals, ActionableGoals,FunctionsEntries

class ActionableGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionableGoals
        fields = ['id', 'purpose', 'grp']

class FunctionGoalSerializer(serializers.ModelSerializer):
    # This fetches all ActionableGoals related to this FunctionGoal
    actionable_goals = ActionableGoalSerializer(source='actionablegoals_set', many=True, read_only=True)

    class Meta:
        model = FunctionsGoals
        fields = ['id', 'Maingoal', 'actionable_goals']

class FunctionDetailSerializer(serializers.ModelSerializer):
    # This fetches all FunctionGoals related to this Function
    functional_goals = FunctionGoalSerializer(source='functionsgoals_set', many=True, read_only=True)

    class Meta:
        model = Functions
        fields = ['id', 'function', 'functional_goals']
        
        
class FunctionsEntriesSerializer(serializers.ModelSerializer):
    # We display the string representation but expect the ID for writes
    status_display = serializers.CharField(source='status.status_name', read_only=True)
    goal_purpose = serializers.CharField(source='goal.purpose', read_only=True)

    class Meta:
        model = FunctionsEntries
        fields = ['id', 'goal', 'goal_purpose', 'Creator', 'date', 'time', 'status', 'status_display', 'note']
        read_only_fields = ['time', 'Creator'] # Creator is usually set via the request user