-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 24, 2025 at 08:14 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bookhive_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `book_id` int(11) NOT NULL,
  `title` varchar(150) NOT NULL,
  `author` varchar(100) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `available_copies` int(11) DEFAULT 0,
  `rent_per_day` decimal(6,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`book_id`, `title`, `author`, `category`, `price`, `available_copies`, `rent_per_day`) VALUES
(1, 'The Alchemist', 'Paulo Coelho', 'Fiction', 350.00, 5, 25.00),
(2, 'Python Programming', 'John Zelle', 'Education', 500.00, 3, 40.00),
(3, 'Atomic Habits', 'James Clear', 'Self-Help', 400.00, 4, 30.00),
(4, 'To Kill a Mockingbird', 'Harper Lee', 'Classic', 320.00, 5, 20.00),
(5, 'Data Science from Scratch', 'Joel Grus', 'Education', 650.00, 2, 45.00),
(6, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 300.00, 6, 25.00),
(7, 'Deep Learning with Python', 'Francois Chollet', 'AI/ML', 800.00, 3, 60.00),
(8, 'Think Like a Monk', 'Jay Shetty', 'Self-Help', 450.00, 5, 35.00),
(9, '1984', 'George Orwell', 'Fiction', 330.00, 4, 25.00),
(10, 'Clean Code', 'Robert C. Martin', 'Programming', 700.00, 4, 50.00),
(11, 'Cracking the Coding Interview', 'Gayle Laakmann McDowell', 'Education', 550.00, 3, 45.00),
(12, 'Pride and Prejudice', 'Jane Austen', 'Classic', 310.00, 5, 20.00),
(13, 'AI Superpowers', 'Kai-Fu Lee', 'AI/ML', 720.00, 2, 55.00),
(14, 'The Psychology of Money', 'Morgan Housel', 'Finance', 400.00, 5, 30.00),
(15, 'Rich Dad Poor Dad', 'Robert Kiyosaki', 'Finance', 380.00, 6, 28.00),
(16, 'Machine Learning Yearning', 'Andrew Ng', 'AI/ML', 770.00, 3, 65.00),
(17, 'Inferno', 'Dan Brown', 'Thriller', 420.00, 4, 32.00),
(18, 'The Subtle Art of Not Giving a F*ck', 'Mark Manson', 'Self-Help', 390.00, 4, 28.00),
(19, 'The Power of Now', 'Eckhart Tolle', 'Spirituality', 410.00, 3, 30.00),
(20, 'Sapiens', 'Yuval Noah Harari', 'History', 800.00, 2, 60.00);

-- --------------------------------------------------------

--
-- Table structure for table `rentals`
--

CREATE TABLE `rentals` (
  `rental_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `rent_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `return_date` date DEFAULT NULL,
  `fine` decimal(6,2) DEFAULT 0.00
) ;

--
-- Dumping data for table `rentals`
--

INSERT INTO `rentals` (`rental_id`, `user_id`, `book_id`, `rent_date`, `due_date`, `return_date`, `fine`) VALUES
(1, 1, 1, '2025-10-01', '2025-10-08', '2025-10-09', 10.00),
(2, 2, 5, '2025-10-02', '2025-10-09', NULL, 0.00),
(3, 3, 9, '2025-10-03', '2025-10-10', '2025-10-10', 0.00),
(4, 4, 16, '2025-10-04', '2025-10-11', NULL, 0.00),
(5, 5, 18, '2025-10-05', '2025-10-12', '2025-10-15', 20.00),
(6, 6, 4, '2025-10-06', '2025-10-13', NULL, 0.00),
(7, 7, 11, '2025-10-07', '2025-10-14', NULL, 0.00),
(8, 8, 12, '2025-10-08', '2025-10-15', NULL, 0.00),
(9, 9, 2, '2025-10-09', '2025-10-16', NULL, 0.00),
(10, 10, 13, '2025-10-10', '2025-10-17', NULL, 0.00),
(11, 1, 6, '2025-10-22', '2025-10-29', '2025-10-22', 0.00);

--
-- Triggers `rentals`
--
DELIMITER $$
CREATE TRIGGER `update_availability` AFTER INSERT ON `rentals` FOR EACH ROW UPDATE books
SET available_copies = available_copies - 1
WHERE book_id = NEW.book_id
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `update_availability_on_return` AFTER UPDATE ON `rentals` FOR EACH ROW BEGIN
    IF NEW.return_date IS NOT NULL THEN
        UPDATE books
        SET available_copies = available_copies + 1
        WHERE book_id = NEW.book_id;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `transaction_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `transaction_date` date DEFAULT curdate()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`transaction_id`, `user_id`, `book_id`, `amount`, `transaction_date`) VALUES
(1, 1, 7, 800.00, '2025-10-01'),
(2, 2, 1, 350.00, '2025-10-03'),
(3, 3, 14, 400.00, '2025-10-04'),
(4, 4, 10, 700.00, '2025-10-05'),
(5, 5, 3, 400.00, '2025-10-06'),
(6, 6, 2, 500.00, '2025-10-08'),
(7, 7, 15, 380.00, '2025-10-09'),
(8, 8, 19, 410.00, '2025-10-10'),
(9, 9, 20, 800.00, '2025-10-12'),
(10, 10, 8, 450.00, '2025-10-13');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `membership_type` enum('regular','premium') DEFAULT 'regular',
  `password` varchar(255) NOT NULL DEFAULT '1234',
  `role` enum('user','admin') NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `name`, `email`, `phone`, `membership_type`, `password`, `role`) VALUES
(1, 'Aarav Sharma', 'aarav@example.com', '9876543210', 'premium', '1234', 'user'),
(2, 'Priya Nair', 'priya@example.com', '9988776655', 'regular', '1234', 'user'),
(3, 'Ravi Patel', 'ravi@example.com', '9123456789', 'regular', '1234', 'user'),
(4, 'Kavya Menon', 'kavya@example.com', '9898989898', 'premium', '1234', 'user'),
(5, 'Rohit Sinha', 'rohit@example.com', '9090909090', 'regular', '1234', 'user'),
(6, 'Sneha Reddy', 'sneha@example.com', '9191919191', 'premium', '1234', 'user'),
(7, 'Vikram Rao', 'vikram@example.com', '9009009000', 'regular', '1234', 'user'),
(8, 'Neha Gupta', 'neha@example.com', '9111111111', 'regular', '1234', 'user'),
(9, 'Aditi Verma', 'aditi@example.com', '9333333333', 'premium', '1234', 'user'),
(10, 'Arjun Mehta', 'arjun@example.com', '9435467766', 'regular', '1234', 'user'),
(11, 'Admin', 'admin@bookhive.com', '7002564925', 'premium', 'admin123', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`book_id`);

--
-- Indexes for table `rentals`
--
ALTER TABLE `rentals`
  ADD PRIMARY KEY (`rental_id`),
  ADD KEY `book_id` (`book_id`),
  ADD KEY `fk_user` (`user_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`transaction_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `email_2` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `book_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `rentals`
--
ALTER TABLE `rentals`
  MODIFY `rental_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `transaction_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `rentals`
--
ALTER TABLE `rentals`
  ADD CONSTRAINT `fk_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `rentals_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `rentals_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE;

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
