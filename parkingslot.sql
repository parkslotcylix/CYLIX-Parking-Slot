-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 01, 2026 at 03:27 PM
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
-- Database: `parkingslot`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `admin_name` varchar(100) NOT NULL,
  `admin_email` varchar(100) NOT NULL,
  `profile_picture` varchar(500) DEFAULT '/static/images/default-profile.png',
  `admin_password` varchar(255) NOT NULL,
  `access_level` enum('super_admin','admin','manager') DEFAULT 'admin',
  `status` enum('active','inactive','suspended') DEFAULT 'active',
  `last_login` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `admin_name`, `admin_email`, `profile_picture`, `admin_password`, `access_level`, `status`, `last_login`, `created_at`, `updated_at`) VALUES
(1, 'Admin Julie', 'juliemay1917@gmail.com', '/static/images/profiles/admin_1_1776449766.jpg', 'Juliemay0!', 'super_admin', 'active', NULL, '2026-04-17 06:27:50', '2026-05-01 13:18:03');

-- --------------------------------------------------------

--
-- Table structure for table `admin_logs`
--

CREATE TABLE `admin_logs` (
  `log_id` int(11) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `action` varchar(100) NOT NULL,
  `slot_id` int(11) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `admin_logs`
--

INSERT INTO `admin_logs` (`log_id`, `admin_id`, `action`, `slot_id`, `description`, `ip_address`, `created_at`) VALUES
(1, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 10:10:57'),
(2, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 10:10:58'),
(3, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 10:10:59'),
(4, 1, 'toggle_slot', 3, 'Status changed to Occupied', NULL, '2026-04-17 10:11:00'),
(5, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 10:11:03'),
(6, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 10:12:07'),
(7, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-04-17 10:12:08'),
(8, 1, 'toggle_slot', 3, 'Status changed to Available', NULL, '2026-04-17 10:12:09'),
(9, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 10:12:10'),
(10, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 10:12:11'),
(11, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 10:14:21'),
(12, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 10:14:22'),
(13, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 10:15:17'),
(14, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 10:15:27'),
(15, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-04-17 10:15:28'),
(16, 1, 'toggle_slot', 3, 'Status changed to Occupied', NULL, '2026-04-17 10:15:28'),
(17, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 10:16:21'),
(18, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-04-17 10:16:22'),
(19, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 10:16:23'),
(20, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 10:16:23'),
(21, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-04-17 10:16:26'),
(22, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 10:16:29'),
(23, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 10:16:30'),
(24, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 10:22:09'),
(25, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 10:22:10'),
(26, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-04-17 10:22:10'),
(27, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 10:22:12'),
(28, 1, 'toggle_slot', 3, 'Status changed to Available', NULL, '2026-04-17 10:22:12'),
(29, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 10:22:14'),
(30, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 10:22:43'),
(31, 1, 'toggle_slot', 3, 'Status changed to Occupied', NULL, '2026-04-17 10:22:44'),
(32, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-04-17 16:43:22'),
(33, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 16:43:23'),
(34, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 16:47:23'),
(35, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 16:47:23'),
(36, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-04-17 16:47:23'),
(37, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 16:47:24'),
(38, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 16:47:25'),
(39, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 16:47:25'),
(40, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-04-17 16:47:27'),
(41, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 16:47:28'),
(42, 1, 'toggle_slot', 3, 'Status changed to Available', NULL, '2026-04-17 16:47:30'),
(43, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 16:47:31'),
(44, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 16:47:31'),
(45, 1, 'toggle_slot', 3, 'Status changed to Occupied', NULL, '2026-04-17 16:47:31'),
(46, 1, 'change_password', NULL, 'Admin changed their password', NULL, '2026-04-17 17:28:25'),
(47, 1, 'change_password', NULL, 'Admin changed their password', NULL, '2026-04-17 17:34:54'),
(48, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 17:43:12'),
(49, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 17:44:32'),
(50, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 17:44:33'),
(51, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-04-17 17:44:33'),
(52, 1, 'toggle_slot', 3, 'Status changed to Available', NULL, '2026-04-17 17:44:34'),
(53, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 17:44:35'),
(54, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 17:44:36'),
(55, 1, 'toggle_slot', 3, 'Status changed to Occupied', NULL, '2026-04-17 17:47:55'),
(56, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-04-17 17:48:47'),
(57, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 17:48:48'),
(58, 1, 'toggle_slot', 3, 'Status changed to Available', NULL, '2026-04-17 17:48:51'),
(59, 1, 'toggle_slot', 3, 'Status changed to Occupied', NULL, '2026-04-17 17:48:52'),
(60, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 18:37:47'),
(61, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 18:37:52'),
(62, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-04-17 18:37:55'),
(63, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 18:37:56'),
(64, 1, 'toggle_slot', 3, 'Status changed to Available', NULL, '2026-04-17 18:37:57'),
(65, 1, 'toggle_slot', 3, 'Status changed to Occupied', NULL, '2026-04-17 18:37:58'),
(66, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 18:40:34'),
(67, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 18:40:35'),
(68, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 18:40:37'),
(69, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 18:40:38'),
(70, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 18:40:40'),
(71, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 18:40:41'),
(72, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 18:42:35'),
(73, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 18:42:38'),
(74, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 18:42:47'),
(75, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 18:42:49'),
(76, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 18:45:00'),
(77, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 18:45:01'),
(78, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 18:45:06'),
(79, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 18:45:07'),
(80, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 19:04:12'),
(81, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 19:04:14'),
(82, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 19:04:15'),
(83, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 19:04:17'),
(84, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-04-17 19:04:45'),
(85, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 19:04:46'),
(86, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 19:06:49'),
(87, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 19:06:50'),
(88, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 19:06:55'),
(89, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 19:06:56'),
(90, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 19:11:28'),
(91, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 19:11:30'),
(92, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 19:15:49'),
(93, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 19:15:51'),
(94, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 19:15:55'),
(95, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 19:15:56'),
(96, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-04-17 19:16:54'),
(97, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-04-17 19:16:55'),
(98, 1, 'toggle_slot', 3, 'Status changed to Available', NULL, '2026-04-17 19:16:57'),
(99, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-04-17 19:16:58'),
(100, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-04-17 19:17:00'),
(101, 1, 'toggle_slot', 3, 'Status changed to Occupied', NULL, '2026-04-18 05:05:01'),
(102, 1, 'toggle_slot', 3, 'Status changed to Available', NULL, '2026-04-18 05:05:01'),
(103, 1, 'toggle_slot', 3, 'Status changed to Occupied', NULL, '2026-04-18 05:05:03'),
(104, 1, 'auto_detect', NULL, 'Automated detection updated 3 slot(s)', NULL, '2026-04-23 09:42:27'),
(105, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:47:20'),
(106, 1, 'auto_detect', NULL, 'Automated detection updated 2 slot(s)', NULL, '2026-04-30 09:47:20'),
(107, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:49:29'),
(108, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:49:30'),
(109, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:06'),
(110, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:06'),
(111, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:07'),
(112, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:07'),
(113, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:07'),
(114, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:07'),
(115, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:07'),
(116, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:07'),
(117, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:07'),
(118, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:07'),
(119, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:08'),
(120, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:08'),
(121, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:27'),
(122, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:28'),
(123, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:32'),
(124, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:32'),
(125, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:37'),
(126, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:37'),
(127, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:37'),
(128, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:38'),
(129, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:41'),
(130, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:41'),
(131, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:43'),
(132, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:43'),
(133, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:50'),
(134, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:50'),
(135, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:51'),
(136, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:52'),
(137, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:54'),
(138, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:54'),
(139, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:55'),
(140, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:55'),
(141, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:55'),
(142, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:50:57'),
(143, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:55:52'),
(144, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:55:53'),
(145, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:15'),
(146, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:15'),
(147, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:16'),
(148, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:16'),
(149, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:16'),
(150, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:17'),
(151, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:30'),
(152, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:30'),
(153, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:33'),
(154, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:33'),
(155, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:35'),
(156, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:36'),
(157, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:38'),
(158, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:38'),
(159, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:43'),
(160, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:43'),
(161, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:46'),
(162, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:47'),
(163, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:50'),
(164, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:50'),
(165, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:59'),
(166, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:56:59'),
(167, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:57:01'),
(168, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:57:01'),
(169, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:57:04'),
(170, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:57:04'),
(171, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:57:05'),
(172, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:57:05'),
(173, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:57:08'),
(174, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:57:08'),
(175, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:57:15'),
(176, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:57:15'),
(177, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:57:15'),
(178, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 09:57:16'),
(179, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 10:12:18'),
(180, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 10:12:46'),
(181, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 10:12:46'),
(182, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 10:12:46'),
(183, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 10:12:46'),
(184, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 10:13:57'),
(185, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 10:13:57'),
(186, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 10:13:57'),
(187, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 10:13:57'),
(188, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 10:14:22'),
(189, 1, 'auto_detect', NULL, 'Automated detection updated 1 slot(s)', NULL, '2026-04-30 10:14:22'),
(190, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-05-01 11:15:03'),
(191, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-05-01 11:15:05'),
(192, 1, 'password_reset', NULL, 'Password was reset via email link', NULL, '2026-05-01 12:22:17'),
(193, 1, 'password_reset', NULL, 'Password was reset via email link', NULL, '2026-05-01 12:25:08'),
(194, 1, 'password_reset', NULL, 'Password was reset via email link', NULL, '2026-05-01 13:09:07'),
(195, 1, 'password_reset', NULL, 'Password was reset via email link', NULL, '2026-05-01 13:18:03'),
(196, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-05-01 13:20:30'),
(197, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-05-01 13:20:31'),
(198, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-05-01 13:20:32'),
(199, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-05-01 13:20:33'),
(200, 1, 'toggle_slot', 1, 'Status changed to Available', NULL, '2026-05-01 13:23:57'),
(201, 1, 'toggle_slot', 2, 'Status changed to Available', NULL, '2026-05-01 13:23:57'),
(202, 1, 'toggle_slot', 2, 'Status changed to Occupied', NULL, '2026-05-01 13:23:58'),
(203, 1, 'toggle_slot', 1, 'Status changed to Occupied', NULL, '2026-05-01 13:23:59');

-- --------------------------------------------------------

--
-- Table structure for table `parking_history`
--

CREATE TABLE `parking_history` (
  `history_id` int(11) NOT NULL,
  `slot_id` int(11) NOT NULL,
  `vehicle_reg_number` varchar(50) DEFAULT NULL,
  `check_in_time` datetime NOT NULL,
  `check_out_time` datetime DEFAULT NULL,
  `duration_hours` decimal(10,2) DEFAULT NULL,
  `parking_fee` decimal(10,2) DEFAULT NULL,
  `status` enum('active','completed','cancelled') DEFAULT 'active',
  `notes` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `parking_rates`
--

CREATE TABLE `parking_rates` (
  `rate_id` int(11) NOT NULL,
  `rate_name` varchar(100) NOT NULL,
  `rate_per_hour` decimal(10,2) NOT NULL,
  `rate_per_day` decimal(10,2) DEFAULT NULL,
  `rate_per_month` decimal(10,2) DEFAULT NULL,
  `status` enum('active','inactive') DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `parking_rates`
--

INSERT INTO `parking_rates` (`rate_id`, `rate_name`, `rate_per_hour`, `rate_per_day`, `rate_per_month`, `status`, `created_at`, `updated_at`) VALUES
(1, 'Hourly Rate', 5.00, 40.00, 150.00, 'active', '2026-04-17 06:27:50', '2026-04-17 06:27:50'),
(2, 'Daily Pass', 15.00, 15.00, 300.00, 'active', '2026-04-17 06:27:50', '2026-04-17 06:27:50'),
(3, 'Monthly Pass', 0.50, 15.00, 300.00, 'active', '2026-04-17 06:27:50', '2026-04-17 06:27:50');

-- --------------------------------------------------------

--
-- Table structure for table `parking_slots`
--

CREATE TABLE `parking_slots` (
  `slot_id` int(11) NOT NULL,
  `slot_number` varchar(50) NOT NULL,
  `slot_label` varchar(100) NOT NULL,
  `slot_status` enum('Available','Occupied','Maintenance') DEFAULT 'Available',
  `vehicle_reg_number` varchar(50) DEFAULT NULL,
  `check_in_time` datetime DEFAULT NULL,
  `check_out_time` datetime DEFAULT NULL,
  `car_image` varchar(255) DEFAULT NULL,
  `location_floor` int(11) DEFAULT NULL,
  `location_zone` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `parking_slots`
--

INSERT INTO `parking_slots` (`slot_id`, `slot_number`, `slot_label`, `slot_status`, `vehicle_reg_number`, `check_in_time`, `check_out_time`, `car_image`, `location_floor`, `location_zone`, `created_at`, `updated_at`) VALUES
(1, 'SLOT-001', 'SLOT 1', 'Occupied', NULL, '2026-05-01 21:23:59', '2026-05-01 21:23:57', 'b-car.png', 1, 'Zone A', '2026-04-17 06:27:50', '2026-05-01 13:23:59'),
(2, 'SLOT-002', 'SLOT 2', 'Occupied', NULL, '2026-05-01 21:23:58', '2026-05-01 21:23:57', 'bl-car.png', 1, 'Zone A', '2026-04-17 06:27:50', '2026-05-01 13:23:58'),
(3, 'SLOT-003', 'SLOT 3', 'Available', NULL, '2026-04-30 18:14:22', '2026-04-30 18:14:22', 'w-car.png', 1, 'Zone A', '2026-04-17 06:27:50', '2026-04-30 10:14:22');

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `token_id` int(11) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL,
  `expires_at` datetime NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `password_reset_tokens`
--

INSERT INTO `password_reset_tokens` (`token_id`, `admin_id`, `token`, `expires_at`, `created_at`) VALUES
(2, 1, 'pu9hg9GCc5y4d6K8Uw22qUyVEt4g513e', '2026-05-01 20:54:02', '2026-05-01 12:24:02'),
(4, 1, 'BmtRM7bobWoB3cbrr90B3kIhP8zIhA7U', '2026-05-01 21:01:55', '2026-05-01 12:31:55'),
(5, 1, 'QwrgQJDUlZjFD2YADf0PReUEgTXNliUz', '2026-05-01 21:07:48', '2026-05-01 12:37:48'),
(6, 1, 'dwAIclBXCoN9PNx8HhMaqxVqZdpQ9CAc', '2026-05-01 21:08:06', '2026-05-01 12:38:06'),
(7, 1, 'I2b0uGDygg7zmhB2pUa25uTQX33MxpsV', '2026-05-01 21:15:55', '2026-05-01 12:45:55');

-- --------------------------------------------------------

--
-- Table structure for table `system_settings`
--

CREATE TABLE `system_settings` (
  `setting_id` int(11) NOT NULL,
  `setting_name` varchar(100) NOT NULL,
  `setting_value` text NOT NULL,
  `setting_type` enum('string','number','boolean','json') DEFAULT 'string',
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `system_settings`
--

INSERT INTO `system_settings` (`setting_id`, `setting_name`, `setting_value`, `setting_type`, `updated_at`) VALUES
(1, 'total_slots', '3', 'number', '2026-04-17 06:27:50'),
(2, 'system_status', 'online', 'string', '2026-04-17 06:27:50'),
(3, 'maintenance_mode', 'false', 'boolean', '2026-04-17 06:27:50'),
(4, 'max_daily_revenue', '1000.00', 'number', '2026-04-17 06:27:50');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `admin_email` (`admin_email`);

--
-- Indexes for table `admin_logs`
--
ALTER TABLE `admin_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `slot_id` (`slot_id`),
  ADD KEY `idx_admin` (`admin_id`),
  ADD KEY `idx_action` (`action`);

--
-- Indexes for table `parking_history`
--
ALTER TABLE `parking_history`
  ADD PRIMARY KEY (`history_id`),
  ADD KEY `slot_id` (`slot_id`),
  ADD KEY `idx_vehicle` (`vehicle_reg_number`),
  ADD KEY `idx_checkin` (`check_in_time`);

--
-- Indexes for table `parking_rates`
--
ALTER TABLE `parking_rates`
  ADD PRIMARY KEY (`rate_id`);

--
-- Indexes for table `parking_slots`
--
ALTER TABLE `parking_slots`
  ADD PRIMARY KEY (`slot_id`),
  ADD UNIQUE KEY `slot_number` (`slot_number`),
  ADD KEY `idx_status` (`slot_status`),
  ADD KEY `idx_floor` (`location_floor`);

--
-- Indexes for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`token_id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indexes for table `system_settings`
--
ALTER TABLE `system_settings`
  ADD PRIMARY KEY (`setting_id`),
  ADD UNIQUE KEY `setting_name` (`setting_name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `admin_logs`
--
ALTER TABLE `admin_logs`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=204;

--
-- AUTO_INCREMENT for table `parking_history`
--
ALTER TABLE `parking_history`
  MODIFY `history_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `parking_rates`
--
ALTER TABLE `parking_rates`
  MODIFY `rate_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `parking_slots`
--
ALTER TABLE `parking_slots`
  MODIFY `slot_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  MODIFY `token_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `system_settings`
--
ALTER TABLE `system_settings`
  MODIFY `setting_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin_logs`
--
ALTER TABLE `admin_logs`
  ADD CONSTRAINT `admin_logs_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`),
  ADD CONSTRAINT `admin_logs_ibfk_2` FOREIGN KEY (`slot_id`) REFERENCES `parking_slots` (`slot_id`);

--
-- Constraints for table `parking_history`
--
ALTER TABLE `parking_history`
  ADD CONSTRAINT `parking_history_ibfk_1` FOREIGN KEY (`slot_id`) REFERENCES `parking_slots` (`slot_id`);

--
-- Constraints for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD CONSTRAINT `password_reset_tokens_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
