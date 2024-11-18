extends Label

const FLY_SPEED = 5.0
const scalar = 50.0
var origin

var target_x = 0
var target_y = 0

# Called when the node enters the scene tree for the first time.
func _ready():
	origin = position

func _physics_process(delta):
	var destination = origin + (Vector2(target_x, target_y) * scalar)
	position = position.lerp(destination, delta * FLY_SPEED)
