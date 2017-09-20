import turtle

def draw_turtle():

	window = turtle.Screen()
	window.bgcolor('blue')

	draw = turtle.Turtle()
	draw.shape('turtle') # the shape of point
	draw.color('red') # the color of point
	draw.speed(5) # the speed of point

	# Draw a square
	for _ in range(4):
		draw.forward(100)
		draw.right(90)

	# Draw a circle
	draw1 = turtle.Turtle()
	draw1.color('white')
	draw1.circle(10) # the number is radius of the circle

	window.exitonclick()

def mindInStrom():

	window = turtle.Screen()

	point = turtle.Turtle()
	point.color('red')
	point.speed(10)

	for _ in range(36):
		for _ in range (4):
			point.forward(100)
			point.right(90)
		point.right(10)

	window.exitonclick()

if __name__ == '__main__':
	# draw_turtle()

	mindInStrom()