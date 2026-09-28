from sklearn.linear_model import LinearRegression


def get_recommendations(current_product, products, limit=3):
    """
    Generate simple ML-based product recommendations
    using Linear Regression.
    """

    products = list(products)

    if len(products) < 2:
        return []

    training_data = []
    target_scores = []

    for product in products:
        same_category = (
            product.category_id == current_product.category_id
        )

        price_difference = abs(
            float(product.price) - float(current_product.price)
        )

        # Feature values
        features = [
            1 if same_category else 0,
            price_difference,
            1 if product.is_featured else 0,
        ]

        training_data.append(features)

        # Simple target score used to train the model
        score = (
            (3 if same_category else 0)
            + (2 if product.is_featured else 0)
            - (price_difference / 10000)
        )

        target_scores.append(score)

    model = LinearRegression()
    model.fit(training_data, target_scores)

    predictions = model.predict(training_data)

    recommendations = []

    for product, prediction in zip(products, predictions):

        if product.id == current_product.id:
            continue

        recommendations.append(
            (product, prediction)
        )

    recommendations.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return [
        product
        for product, score in recommendations[:limit]
    ]