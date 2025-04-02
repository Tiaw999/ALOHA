-- Insert sample stores
INSERT INTO stores (storename, password) 
VALUES ('aloha', 'storepass1'), ('aloha2', 'storepass2'), ('aloha3', 'storepass3');

-- Insert sample staff
INSERT INTO staff (name, storename, hourlyrate, bonusrate, password, role) 
VALUES
    ('owner1', 'aloha', '25', '0.03', 'password123', 'Owner'),
    ('manager1', 'aloha2', '20', '.02', 'password123', 'Manager'),
    ('employee1', 'aloha3', '15', '.01', 'password123', 'Employee');
