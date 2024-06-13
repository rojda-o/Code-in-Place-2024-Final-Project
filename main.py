import tkinter as tk
import random

#Constants
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400
SIZE = 20
SPEED = 50

def main():
    root = tk.Tk()
    root.title("Snake Game")

    # Create the canvas
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
    canvas.pack()

    def create_snake(): #creating a snake with a size of 3 body parts
        body_size = 3
        coordinates = []  # list to store the coordinates of the snake's body parts
        squares = []   #list to store snake's body parts(squares)

        for i in range(body_size):
            coordinates.append([0, 0])

        for x, y in coordinates:
            square = canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill="blue")
            squares.append(square)

        return coordinates, squares

    #creating a food randomly inside the borders of the canvas
    def create_food():
        food_x = random.randint(0, (CANVAS_WIDTH // SIZE) - 1) * SIZE
        food_y = random.randint(0, (CANVAS_HEIGHT // SIZE) - 1) * SIZE
        canvas.create_rectangle(food_x, food_y, food_x + SIZE, food_y + SIZE, fill="red", tag="food")

        food_coordinates = [food_x,food_y]
        return food_coordinates

    def next_turn(coordinates, squares, food_coords):
        x, y = coordinates[0]

        if direction == "up":
            y -= SIZE
        elif direction == "down":
            y += SIZE
        elif direction == "left":
            x -= SIZE
        elif direction == "right":
            x += SIZE

        coordinates.insert(0, (x, y))
        square = canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill="blue")
        squares.insert(0, square)

        if x == food_coords[0] and y == food_coords[1]: #if they're overlapping
            nonlocal  score
            score += 1
            label.config(text = "Score: {}".format(score))
            canvas.delete("food")
            food_coords = create_food()
        else:
            del coordinates[-1]
            canvas.delete(squares[-1])
            del squares[-1]

        #to keep the snake inside the canvas
        if x<0 or x >= CANVAS_WIDTH:
            game_over()
        elif y <0 or y >= CANVAS_HEIGHT:
            game_over()
        #if snake is overlapping itself
        else:
            for body_part in coordinates[1:]:  #for every body part after the head of the snake
                if x == body_part[0] and y == body_part[1]:
                    game_over()
            else:
                root.after(SPEED, next_turn, coordinates,  squares, food_coords)

    #a function to change direction when a key is pressed
    def change_direction(new_direction):
        nonlocal direction

        if new_direction == 'left':
            if direction != 'right':  #for not to go backwards
                direction = new_direction
        elif new_direction == 'right':
            if direction != 'left':
                direction = new_direction
        elif new_direction == 'up':
            if direction != 'down':
                direction = new_direction
        elif new_direction == 'down':
            if direction != 'up':
                direction = new_direction

    #if the game is over we clear the canvas and display "GAME OVER"
    def game_over():
        canvas.delete("all")
        canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, font=('Comic Sans MS', 60), text="GAME OVER", fill="blue")

    score = 0 #to keep the score
    direction = 'down' #snake starts to move in this direction

    #a label to show the score
    label = tk.Label(root, text="Score: {}".format(score), font=('Comic Sans MS', 30))
    label.pack()

    root.bind('<Left>', lambda event: change_direction('left'))
    root.bind('<Right>', lambda event: change_direction('right'))
    root.bind('<Up>', lambda event: change_direction('up'))
    root.bind('<Down>', lambda event: change_direction('down'))

    #creating the snake and a food, getting the coordinates
    coordinates, squares = create_snake()
    food_coords = create_food()
    next_turn(coordinates, squares, food_coords)

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
