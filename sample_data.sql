-- Insert sample stores
INSERT INTO stores (storename)
VALUES ('aloha'), ('aloha2');

-- Insert sample staff
INSERT INTO staff (name, storename, hourlyrate, bonusrate, password, role) 
VALUES
    ('owner1', 'aloha', '25', '0.03', 'password123', 'Owner'),
    ('manager1', 'aloha2', '20', '.02', 'password123', 'Manager')
