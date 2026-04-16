--
-- Database: `sign_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `mobile` varchar(15) default NULL,
  `age` int(11) default NULL,
  `gender` varchar(10) default NULL,
  `dob` date default NULL,
  `location` varchar(100) default NULL,
  `username` varchar(50) default NULL,
  `password` varchar(100) default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `mobile`, `age`, `gender`, `dob`, `location`, `username`, `password`) VALUES
(2, 'Vijay', 'vijay@gmail.com', '8764312346', 19, 'Male', '2003-04-14', 'Trichy', 'vijay', '1234');
