-- Create Customers table
CREATE TABLE User
(
    UserID   INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(51) UNIQUE NOT NULL,
    password VARCHAR(255)       NOT NULL
);
CREATE TABLE Customers
(
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    UserID     INT                 NOT NULL,
    Name       VARCHAR(255)        NOT NULL,
    Email      VARCHAR(255) UNIQUE NOT NULL,
    Phone      VARCHAR(20),
    Check (LENGTH(Phone) <= 20),
    FOREIGN KEY (UserID) REFERENCES User (UserID)

);

-- Create VehicleTypes table
CREATE TABLE VehicleTypes
(
    VehicleTypeID      INT AUTO_INCREMENT PRIMARY KEY,
    Type               VARCHAR(50) NOT NULL,
    VehicleMaxCapacity INT         NULL
);

-- Create Vehicles table
CREATE TABLE Vehicles
(
    VehicleID     INT AUTO_INCREMENT PRIMARY KEY,
    VehicleTypeID INT     NOT NULL,
    Price         DECIMAL NOT NULL,
    Availability  BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (VehicleTypeID) REFERENCES VehicleTypes (VehicleTypeID)
);

-- Create Bookings table
CREATE TABLE Bookings
(
    BookingID  INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    VehicleID  INT,
    Price      DECIMAL NOT NULL,
    DateOfHire DATE    NOT NULL,
    ReturnDate DATE    NOT NULL,
    Check (ReturnDate >= DateOfHire),
    FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles (VehicleID)
);
#
# -- Sample data for Customers
# INSERT INTO Customers (Name, Email, Phone)
# VALUES ('Ahmed', 'ahmed@example.com', '00201060444567'),
#        ('Samy', 'samy@example.com', '0123123123123');
#
# -- Sample data for VehicleTypes
# INSERT INTO VehicleTypes (Type, VehicleMaxCapacity)
# VALUES ('small', 2),
#        ('family', 7),
#        ('van', null);
#
# -- Sample data for Vehicles
# INSERT INTO Vehicles (Type, VehicleTypeID, Availability)
# VALUES ('Small Car Available', 1, true),
#        ('Small Car Not Available', 1, false),
#        ('Family Car Available', 2, true),
#        ('Family Car Not Available', 2, false),
#        ('Van Available', 3, true),
#        ('Van Not Available', 3, false);
