Globant Test
************

### Dependencies for program LoaderHisto.py	
yum -y install mariadb-connector-c
yum -y install mariadb-connector-c-devel
yum -y install gcc
yum -y install python3-devel
pip3 install mariadb
pip3 install flask
pip3 install flask_restful
pip3 install socket

### Previous
For security reasons is necessary set the following environmental variables to run LoaderHisto.py:
DBUSER, DBPASSWORD, DBHOST, DBPORT and DBNAME
Develop in Python 3.6

### Loading Hisotry Data from csv file:
The LoaderHisto.py module take the files jobs.csv, departments.csv and hired_employees.csv
and load into a local mariadb (credential are public riskly temporarily).

Files with format input error where employee_error.txt, job_error.txt and department_error.txt


### Loading Data by POST request method

POST Method 
URL: http://131.221.33.50:5000/loader
Body raw JSON Data: [{"txnType":"job","id":184,"job":"Cleaning floor and windows"},
{"txnType":"employee","id":2000,"name":"Juan Ramos","datetime":"2022-01-07T13:13:18Z","department_id":3,"job_id":3},
{"txnType":"department","id":13,"department":"Cleaning Department"}]

In order to reach 1000, the files must be increased in the body raw JSON Data.

CURL invocation
curl --location --request POST 'http://131.221.33.50:5000/loader' \
--header 'Content-Type: application/json' \
--data-raw '[{"txnType":"job","id":184,"job":"Cleaning floor and windows"},
{"txnType":"employee","id":2000,"name":"Juan Ramos","datetime":"2022-01-07T13:13:18Z","department_id":3,"job_id":3},
{"txnType":"department","id":13,"department":"Cleaning Department"}]'



#### DATABASE MariaDB ######
The tables created and loaded were company.department, company.job and company.empoyee with foreign key pointing to the dependenies.

CREATE TABLE `job` (
	`id` INT(10) UNSIGNED NOT NULL,
	`job` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='latin1_swedish_ci'
ENGINE=InnoDB
;

CREATE TABLE `department` (
	`id` INT(10) UNSIGNED NOT NULL,
	`department` VARCHAR(50) NOT NULL DEFAULT 'NOT VALUE' COLLATE 'latin1_swedish_ci',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='latin1_swedish_ci'
ENGINE=InnoDB
;

CREATE TABLE `employee` (
        `id` INT(11) NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_swedish_ci',
        `datetime` DATETIME NULL DEFAULT NULL,
        `department_id` INT(10) UNSIGNED NOT NULL DEFAULT '0',
        `job_id` INT(10) UNSIGNED NOT NULL DEFAULT '0',
        PRIMARY KEY (`id`) USING BTREE,
        INDEX `FK__job` (`job_id`) USING BTREE,
        INDEX `FK__department` (`department_id`) USING BTREE,
        CONSTRAINT `FK__department` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`) ON UPDATE RESTRICT ON DELETE CASCADE,
        CONSTRAINT `FK__job` FOREIGN KEY (`job_id`) REFERENCES `job` (`id`) ON UPDATE RESTRICT ON DELETE CASCADE
)
COLLATE='latin1_swedish_ci'
ENGINE=InnoDB
AUTO_INCREMENT=2000
;

#END OF README
# This is property of www.raicotech.cl all right reserved
