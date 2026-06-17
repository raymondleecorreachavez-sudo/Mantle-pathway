import numpy as np
from pydantic import BaseModel, field_validator

class BaseStiffnessTensor(BaseModel):
    matrix: list[list[float]]
    density: float

    @field_validator('matrix')
    @classmethod
    def validate_dimensions(cls, v):
        arr = np.array(v)
        if arr.shape != (6, 6):
            raise ValueError("Stiffness matrix must be exactly 6x6.")
        if not np.allclose(arr, arr.T, atol=1e-8):
            raise ValueError("Stiffness matrix must be symmetric (C_ij = C_ji).")
        return v

    def to_numpy(self) -> np.ndarray:
        return np.array(self.matrix)

class HexagonalTensor(BaseStiffnessTensor):
    @field_validator('matrix')
    @classmethod
    def validate_hexagonal(cls, v):
        arr = np.array(v)
        # Check C12 = C11 - 2*C66
        if not np.isclose(arr[0, 1], arr[0, 0] - 2 * arr[5, 5]):
            raise ValueError("Hexagonal symmetry requires C12 = C11 - 2*C66")
        return v

class OrthorhombicTensor(BaseStiffnessTensor):
    pass # Standard 6x6 validation from base is sufficient for structural layout

class CubicTensor(BaseStiffnessTensor):
    @field_validator('matrix')
    @classmethod
    def validate_cubic(cls, v):
        arr = np.array(v)
        if not (arr[0,0] == arr[1,1] == arr[2,2]):
            raise ValueError("Cubic symmetry requires C11 = C22 = C33")
        if not (arr[3,3] == arr[4,4] == arr[5,5]):
            raise ValueError("Cubic symmetry requires C44 = C55 = C66")
        return v
