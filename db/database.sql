-- Disable foreign key checks
SET CONSTRAINTS ALL DEFERRED;

-- Table structure for table users
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(50)  NOT NULL,
    mobile      VARCHAR(15)  NULL UNIQUE,
    email       VARCHAR(64)  NOT NULL UNIQUE,
    password    VARCHAR(100) NOT NULL,
    profile     VARCHAR(255),
    is_verified BOOLEAN   DEFAULT FALSE,
    verified_at TIMESTAMP,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table structure for table roles
DROP TABLE IF EXISTS roles CASCADE;
CREATE TABLE roles
(
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table structure for table user_role
DROP TABLE IF EXISTS user_role CASCADE;
CREATE TABLE user_role
(
    id         SERIAL PRIMARY KEY,
    users_id   INT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    roles_id   INT NOT NULL REFERENCES roles (id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table structure for table users_address
DROP TABLE IF EXISTS users_address CASCADE;
CREATE TABLE users_address
(
    id           SERIAL PRIMARY KEY,
    users_id     INT          NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    state        VARCHAR(150) NOT NULL,
    city         VARCHAR(150) NOT NULL,
    country      VARCHAR(100) NOT NULL,
    zip_code     VARCHAR(6)   NOT NULL,
    address_1    TEXT         NOT NULL,
    address_2    TEXT,
    landmark     VARCHAR(200),
    is_default   BOOLEAN      NOT NULL DEFAULT FALSE,
    is_deleted   BOOLEAN      NOT NULL DEFAULT FALSE,
    address_type VARCHAR(10) CHECK (address_type IN ('Home', 'Office', 'Other')),
    created_at   TIMESTAMP             DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP             DEFAULT CURRENT_TIMESTAMP
);

-- Table structure for table category
DROP TABLE IF EXISTS category CASCADE;
CREATE TABLE category
(
    id          SERIAL PRIMARY KEY,
    parent_id   INT,
    name        VARCHAR(255) NOT NULL,
    description TEXT         NOT NULL,
    image       VARCHAR(255) NOT NULL,
    sort_order  INT,
    active      BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP             DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP             DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES category (id) ON DELETE CASCADE
);

-- Table structure for table category_tag
DROP TABLE IF EXISTS category_tag CASCADE;
CREATE TABLE category_tag
(
    id           SERIAL PRIMARY KEY,
    category_id  INT NOT NULL REFERENCES category (id) ON DELETE CASCADE,
    seo_title    VARCHAR(255),
    seo_desc     TEXT,
    seo_keywords VARCHAR(255),
    h1_tag       VARCHAR(255),
    h2_tag       VARCHAR(255),
    h3_tag       VARCHAR(255),
    alt_img_tag  VARCHAR(255)
);

-- Table structure for table attribute
DROP TABLE IF EXISTS attribute CASCADE;
CREATE TABLE attribute
(
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(255) NOT NULL,
    sort_order INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table structure for table coupon
DROP TABLE IF EXISTS coupon CASCADE;
CREATE TABLE coupon
(
    id           SERIAL PRIMARY KEY,
    code         VARCHAR(255)                                                NOT NULL,
    description  TEXT,
    active       BOOLEAN   DEFAULT TRUE,
    coupon_type  VARCHAR(20) CHECK (coupon_type IN ('Amount', 'Percentage')) NOT NULL,
    coupon_value NUMERIC                                                     NOT NULL,
    sort_order   INT,
    start_at     TIMESTAMP                                                   NOT NULL,
    end_at       TIMESTAMP                                                   NOT NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table structure for table product
DROP TABLE IF EXISTS product CASCADE;
CREATE TABLE product
(
    id          SERIAL PRIMARY KEY,
    category_id INT          NOT NULL REFERENCES category (id) ON DELETE CASCADE,
    name        VARCHAR(255) NOT NULL,
    sku         VARCHAR(10)  NOT NULL,
    description TEXT         NOT NULL,
    active      BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP             DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP             DEFAULT CURRENT_TIMESTAMP
);

-- Table structure for table product_meta
DROP TABLE IF EXISTS product_meta CASCADE;
CREATE TABLE product_meta
(
    id             SERIAL PRIMARY KEY,
    product_id     INT           NOT NULL REFERENCES product (id) ON DELETE CASCADE,
    quantity       INT           NOT NULL,
    original_price DECIMAL(6, 2) NOT NULL,
    discount_price DECIMAL(6, 2),
    tax_percentage DECIMAL(6, 2),
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table structure for table product_img
DROP TABLE IF EXISTS product_img CASCADE;
CREATE TABLE product_img
(
    id          SERIAL PRIMARY KEY,
    product_id  INT                                                 NOT NULL REFERENCES product (id) ON DELETE CASCADE,
    img         VARCHAR(255)                                        NOT NULL,
    thumb_img   VARCHAR(255)                                        NOT NULL,
    file_type   VARCHAR(10) CHECK (file_type IN ('Image', 'Video')) NOT NULL DEFAULT 'Image',
    alt_img_tag VARCHAR(255)                                        NOT NULL,
    sort_order  INT
);

-- Table structure for table product_attribute
DROP TABLE IF EXISTS product_attribute CASCADE;
CREATE TABLE product_attribute
(
    id           SERIAL PRIMARY KEY,
    product_id   INT NOT NULL REFERENCES product (id) ON DELETE CASCADE,
    attribute_id INT NOT NULL REFERENCES attribute (id) ON DELETE CASCADE
);

-- Table structure for table product_tag
DROP TABLE IF EXISTS product_tag CASCADE;
CREATE TABLE product_tag
(
    id           SERIAL PRIMARY KEY,
    product_id   INT          NOT NULL REFERENCES product (id) ON DELETE CASCADE,
    seo_title    VARCHAR(255),
    seo_desc     TEXT         NOT NULL,
    seo_keywords VARCHAR(255),
    h1_tag       VARCHAR(255),
    h2_tag       VARCHAR(255),
    h3_tag       VARCHAR(255),
    alt_img_tag  VARCHAR(255) NOT NULL
);

-- Table structure for table user_cart
DROP TABLE IF EXISTS user_cart CASCADE;
CREATE TABLE user_cart
(
    id         SERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES product (id) ON DELETE CASCADE,
    users_id   INT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    coupon_id  INT NOT NULL,
    quantity   INT NOT NULL
);

-- Table structure for table order_status
DROP TABLE IF EXISTS order_status CASCADE;
CREATE TABLE order_status
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Table structure for table user_order
DROP TABLE IF EXISTS user_order CASCADE;
CREATE TABLE user_order
(
    id               SERIAL PRIMARY KEY,
    users_id         INT           NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    users_address_id INT           NOT NULL REFERENCES users_address (id) ON DELETE CASCADE,
    coupon_id        INT           NOT NULL REFERENCES coupon (id) ON DELETE CASCADE,
    order_status_id  INT           NOT NULL REFERENCES order_status (id) ON DELETE CASCADE,
    delivery_charge  DECIMAL(6, 2) NOT NULL,
    payment_mode     VARCHAR(50),
    transaction_id   VARCHAR(50),
    delivery_at      TIMESTAMP,
    order_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table structure for table order_product
DROP TABLE IF EXISTS order_product CASCADE;
CREATE TABLE order_product
(
    id            SERIAL PRIMARY KEY,
    user_order_id INT          NOT NULL REFERENCES user_order (id) ON DELETE CASCADE,
    product_id    INT          NOT NULL REFERENCES product (id) ON DELETE CASCADE,
    product_name  VARCHAR(255) NOT NULL,
    quantity      INT          NOT NULL,
    product
