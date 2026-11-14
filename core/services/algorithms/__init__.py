from .least_loaded import allocate_least_loaded
from .round_robin import allocate_round_robin
from .skill_match import allocate_skill_match

ALGORITHM_CHOICES = (
    ("round_robin", "Round robin"),
    ("skill_match", "Skill match"),
    ("least_loaded", "Least loaded"),
)

ALGORITHM_FUNCTIONS = {
    "round_robin": allocate_round_robin,
    "skill_match": allocate_skill_match,
    "least_loaded": allocate_least_loaded,
}
