# YLIE

The "Yield Linear Interpolation Engine" (YLIE) is a tool designed to derive yield rates for maturities that lie between available yield curve data points. 

Using "on-the-run" or "off-the-run" fixed income securities data, YLIE is capable of deriving atyipical maturity yields as well as typical "full-maturity" yields.

The module operates by generating and populating a matrix of yield curve data points which are then processed using linear interpolation in order to derive missing yield data points.

YLIE was designed to optimize the valuation process of Fixed Income Instruments when dealing with a large baskets of securties. 
Used in conjuntion with a python data extraction library for Excel and an SQL database, this tool becomes a powerful asset in automating the discount rate calculation process and streamling fixed income valuation workflows.  

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The only dependency is Python 2.x

### Installing

Options to install the YLIE module:

* Clone the repository: git clone https://github.com/mkrahal/YLIE
* Download the zip: https://github.com/mkrahal/YLIE

## Built With

* Python 2.7

## Authors

* **MK Rahal** - *Initial Development* - [mkrahal](https://github.com/mkrahal)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


