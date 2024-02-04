import numpy as np
from matplotlib import pyplot as plt
import random

# Lego constants
track_unit_length = 1.0
corner_radius = 2 * track_unit_length

def main():
    while True:
        generate_track()

def generate_track():
    null_track = TrackSection("")
    track = TrackSection("")

    while len(track) < 50:
        new_piece = random.choice("LRS")

        track += new_piece

        if track == null_track:
            track.save_image()
            return


class TrackGenerator():
    def __init__(self):
        pass

class TrackSection():
    def __init__(self,track_pieces):

        self.track_pieces = track_pieces

        self.transform_matrix = self.compute_total_transform_matrix_from_picecs(self.track_pieces)

    def compute_total_transform_matrix_from_picecs(self, track_pieces):
        total_transform_matrix = np.eye(3)
        for track_piece in track_pieces:
            track_piece_transform = track_piece_transforms[track_piece]
            total_transform_matrix = total_transform_matrix@track_piece_transform
        return total_transform_matrix

    def __add__(self, other):

        if isinstance(other,str):
            other = TrackSection(other)

        new_track_section = TrackSection("")
        new_track_section.track_pieces = self.track_pieces + other.track_pieces
        new_track_section.transform_matrix = self.transform_matrix @ other.transform_matrix

        return new_track_section
    
    def __len__(self):
        return len(self.track_pieces)
            
    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        return hash((self.transform_matrix.round(3)+0).tobytes())
    
    def save_image(self):
        xs = [0]
        ys = [0]
        total_transform_matrix = np.eye(3)
        for track_piece in self.track_pieces:
            track_piece_transform = track_piece_transforms[track_piece]
            total_transform_matrix = total_transform_matrix@track_piece_transform

            xs.append(total_transform_matrix[0,2])
            ys.append(total_transform_matrix[1,2])

        fig, axes= plt.subplots()
        axes.plot(xs,ys)
        axes.set_aspect("equal","box")
        fig.savefig("images/"+self.track_pieces+".png")

def create_corner_piece_transform(rotation_deg):

    cos = np.cos(np.radians(rotation_deg))
    sin = np.sin(np.radians(rotation_deg))
    sign = np.sign(rotation_deg)
    
    r = corner_radius

    transform_matrix = np.array([
        [ cos , -sin , sign*r*sin    ],
        [ sin ,  cos , sign*r*(1-cos)],
        [ 0   ,  0   , 1             ],
    ])

    return transform_matrix

def create_straight_piece_transform(length_in_units):

    x = length_in_units * track_unit_length

    transform_matrix = np.array(
        [
            [1 , 0 , x ],
            [0 , 1 , 0 ],
            [0 , 0 , 1 ],
        ]
    )

    return transform_matrix

track_piece_transforms = {
    "L": create_corner_piece_transform(30),
    "l": create_corner_piece_transform(15),
    "R": create_corner_piece_transform(-30),
    "r": create_corner_piece_transform(-15),
    "S": create_straight_piece_transform(1.0),
    "s": create_straight_piece_transform(0.5),
}

main()

