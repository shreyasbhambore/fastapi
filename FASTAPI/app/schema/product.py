from datetime import datetime
from typing import Annotated, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, computed_field, field_validator, model_validator


class Dimension(BaseModel):
    length: Optional[float] = Field(
        default=None,
        gt=0,
        title="Length",
        description="The length of the product in centimeters.",
        example=35.5,
    )
    width: Optional[float] = Field(
        default=None,
        gt=0,
        title="Width",
        description="The width of the product in centimeters.",
        example=20.0,
    )
    height: Optional[float] = Field(
        default=None,
        gt=0,
        title="Height",
        description="The height of the product in centimeters.",
        example=5.0,
    )


class Product(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: UUID) -> UUID:
        return value

    @model_validator(mode="after")
    def validate_product(self) -> "Product":
        if self.name and len(self.name.strip()) < 1:
            raise ValueError("name cannot be blank")
        return self

    @computed_field
    @property
    def display_name(self) -> str:
        return f"{self.name} - ${self.price:.2f}"

    @computed_field
    @property
    def volume(self) -> Optional[float]:
        if self.dimension is None:
            return None
        return self.dimension.length * self.dimension.width * self.dimension.height

    @computed_field
    @property
    def computed_dimension(self) -> Optional[Dimension]:
        return self.dimension

    name: Annotated[
        str,
        Field(
            ...,
            min_length=1,
            max_length=100,
            title="Product Name",
            description="The name of the product",
            examples=["Laptop", "Smartphone", "Tablet"],
        ),
    ]
    price: Annotated[
        float,
        Field(
            ...,
            gt=0,
            title="Product Price",
            description="The price of the product in USD. Must be greater than zero.",
            example=199.99,
        ),
    ]
    description: Optional[str] = Field(
        None,
        min_length=10,
        max_length=500,
        title="Product Description",
        description="A detailed description of the product.",
        example="A powerful laptop with 16GB RAM, 512GB SSD, and a long-lasting battery.",
    )
    image_urls: List[Annotated[
        str,
        Field(
            min_length=5,
            max_length=2048,
            description="A URL that points to a product image.",
            example="https://example.com/images/laptop.png",
        ),
    ]] = Field(
        default_factory=list,
        title="Product Image URLs",
        description="A list of image URLs for the product.",
    )
    seller: Optional["Seller"] = Field(
        default=None,
        title="Seller",
        description="The seller associated with this product.",
    )
    dimension: Optional[Dimension] = Field(
        default=None,
        title="Product Dimensions",
        description="The physical dimensions of the product.",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        title="Creation Timestamp",
        description="The timestamp when the product was created.",
        example="2023-01-01T12:00:00Z",
    )


class Seller(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: Optional[Annotated[
        str,
        Field(
            default=None,
            min_length=1,
            max_length=100,
            title="Seller Name",
            description="The name of the seller",
            example="Tech Store",
        ),
    ]] = None
    email: Optional[Annotated[
        str,
        Field(
            default=None,
            min_length=5,
            max_length=255,
            title="Seller Email",
            description="The email address of the seller",
            example="seller@example.com",
        ),
    ]] = None
    phone: Optional[str] = Field(
        None,
        min_length=5,
        max_length=20,
        title="Seller Phone",
        description="The phone number of the seller",
        example="+1234567890",
    )
    is_active: bool = Field(
        default=True,
        title="Active Status",
        description="Whether the seller account is active",
    )