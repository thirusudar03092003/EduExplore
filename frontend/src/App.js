import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [courses, setCourses] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [cart, setCart] = useState([]);
  const [matchedCourses, setMatchedCourses] = useState([]);

  // Fetch courses from the backend API
  const fetchCourses = async (query = '', category = '') => {
    try {
      const response = await axios.get('http://localhost:5000/api/courses', {
        params: { query, category },
      });
      setCourses(response.data.data);
      setCategories(response.data.categories);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  };

  // Fetch recommended courses based on course ID
  const fetchRecommendations = async (courseId) => {
    try {
      const response = await axios.get(`http://localhost:5000/api/recommendations/${courseId}`);
      setMatchedCourses(response.data.data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  // Lifecycle: Fetch all courses on component mount
  useEffect(() => {
    fetchCourses();
  }, []);

  // Search and Category Handlers
  const handleSearch = (e) => {
    const query = e.target.value;
    setSearchQuery(query);
    fetchCourses(query, selectedCategory);
  };

  const handleCategoryChange = (e) => {
    const category = e.target.value;
    setSelectedCategory(category);
    fetchCourses(searchQuery, category);
  };

  // Cart Management
  const addToCart = (course) => {
    if (!cart.some((item) => item.id === course.id)) {
      setCart([...cart, course]);
      fetchRecommendations(course.id);  // Fetch recommendations after adding to cart
      alert(`${course.name} added to cart!`);
    } else {
      alert(`${course.name} is already in your cart.`);
    }
  };

  const removeFromCart = (courseId) => {
    setCart(cart.filter((item) => item.id !== courseId));
  };

  const handleCheckout = () => {
    if (cart.length === 0) {
      alert('Your cart is empty!');
    } else {
      alert('Proceeding to checkout...');
    }
  };

  return (
    <div className="container">
      <header>
        <h1>Welcome to Edu-Explore</h1>
        <center><p>Discover online courses and enhance your skills across various domains.</p></center>
      </header>

      {/* Search and Filter */}
      <div className="search-section">
        <input
          type="text"
          placeholder="Search courses..."
          value={searchQuery}
          onChange={handleSearch}
        />
        <select onChange={handleCategoryChange} value={selectedCategory}>
          <option value="">All Categories</option>
          {categories.map((category) => (
            <option key={category} value={category}>
              {category}
            </option>
          ))}
        </select>
      </div>

      {/* Course List */}
      <div className="course-list">
        {courses.length > 0 ? (
          courses.map((course) => (
            <div key={course.id} className="course-card">
              <h3>{course.name}</h3>
              <p>{course.instructor}</p>
              <p>{course.description}</p>
              <p>${course.price.toFixed(2)}</p>
              <button onClick={() => addToCart(course)}>Buy Now</button>
            </div>
          ))
        ) : (
          <p>No courses found.</p>
        )}
      </div>

      {/* Recommended Courses */}
      {matchedCourses.length > 0 && (
        <div className="matched-courses">
          <h2>Recommended Courses</h2>
          <div className="course-list">
            {matchedCourses.map((course) => (
              <div key={course.id} className="course-card">
                <h3>{course.name}</h3>
                <p>{course.instructor}</p>
                <p>{course.description}</p>
                <p>${course.price.toFixed(2)}</p>
                <button onClick={() => addToCart(course)}>Buy Now</button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Cart Section */}
      <div className="cart-section">
        <h2>Your Cart</h2>
        {cart.length === 0 ? (
          <p>Your cart is empty.</p>
        ) : (
          <ul>
            {cart.map((item) => (
              <li key={item.id}>
                {item.name} - ${item.price.toFixed(2)}
                <button onClick={() => removeFromCart(item.id)}>Remove</button>
              </li>
            ))}
          </ul>
        )}
        {cart.length > 0 && <button onClick={handleCheckout}>Proceed to Checkout</button>}
      </div>
    </div>
  );
};

export default App;
