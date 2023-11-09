classDiagram
direction BT
class Bookings {
   int CustomerID
   int VehicleID
   decimal(10) Price
   date DateOfHire
   date ReturnDate
   int BookingID
}
class Customers {
   int UserID
   varchar(255) Name
   varchar(255) Email
   varchar(20) Phone
   int CustomerID
}
class User {
   varchar(51) username
   varchar(255) password
   int UserID
}
class VehicleTypes {
   varchar(50) Type
   int VehicleMaxCapacity
   int VehicleTypeID
}
class Vehicles {
   int VehicleTypeID
   decimal(10) Price
   tinyint(1) Availability
   int VehicleID
}

Bookings  -->  Customers : CustomerID
Bookings  -->  Vehicles : VehicleID
Customers  -->  User : UserID
Vehicles  -->  VehicleTypes : VehicleTypeID
