import argparse
import os
import pickle

import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import (cross_val_score, learning_curve,
                                     train_test_split)
from sklearn.neighbors import KNeighborsClassifier


def evaluate_once(X_train, X_test, y_train, y_test):
    knn = KNeighborsClassifier(n_neighbors=5)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    voting = VotingClassifier(estimators=[('knn', knn), ('rf', rf)], voting='hard')

    voting.fit(X_train, y_train)

    y_pred = voting.predict(X_test)
    acc = voting.score(X_test, y_test)

    return voting, acc, y_pred


def plot_learning_curve(estimator, X, y, cv, output_file):
    train_sizes, train_scores, val_scores = learning_curve(
        estimator, X, y, cv=cv, scoring='accuracy', n_jobs=-1,
        train_sizes=[0.1, 0.25, 0.5, 0.75, 1.0], shuffle=True, random_state=42
    )

    train_mean = train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    val_mean = val_scores.mean(axis=1)
    val_std = val_scores.std(axis=1)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1)
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1)
    plt.plot(train_sizes, train_mean, 'o-', label='Train')
    plt.plot(train_sizes, val_mean, 'o-', label='Validation')
    plt.title(f'Learning curve (cv={cv})')
    plt.xlabel('Training set size')
    plt.ylabel('Accuracy')
    plt.ylim(0, 1.0)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(output_file)


def main():
    parser = argparse.ArgumentParser(description='Evaluate face recognition model and optionally plot accuracy.')
    parser.add_argument('--plot', action='store_true', help='Generate and save an accuracy plot (cross-validated).')
    parser.add_argument('--learning-curve', action='store_true', help='Generate and save a learning curve plot (train vs validation accuracy by training size).')
    parser.add_argument('--plot-file', default='output/accuracy.png', help='Path to save the accuracy plot.')
    parser.add_argument('--curve-file', default='output/learning_curve.png', help='Path to save the learning curve plot.')
    parser.add_argument('--cv', type=int, default=5, help='Number of cross-validation folds when plotting.')
    args = parser.parse_args()

    # Load dataset
    with open('data/names.pkl', 'rb') as f:
        labels = pickle.load(f)
    with open('data/faces_data.pkl', 'rb') as f:
        faces = pickle.load(f)

    # Make sure we have matching sizes
    m = min(len(labels), len(faces))
    faces = faces[:m]
    labels = labels[:m]

    # Split into train/test
    X_train, X_test, y_train, y_test = train_test_split(
        faces, labels, test_size=0.2, stratify=labels, random_state=42
    )

    voting, acc, y_pred = evaluate_once(X_train, X_test, y_train, y_test)
    train_acc = voting.score(X_train, y_train)

    print('Train set size:', len(y_train))
    print('Train accuracy:', train_acc)
    print('\nTest set size:', len(y_test))
    print('Test accuracy:', acc)
    print('\nClassification report:')
    print(classification_report(y_test, y_pred))
    print('Confusion matrix:')
    print(confusion_matrix(y_test, y_pred))

    if args.plot:
        # Compute cross-validated accuracy for a stability plot
        knn = KNeighborsClassifier(n_neighbors=5)
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        voting = VotingClassifier(estimators=[('knn', knn), ('rf', rf)], voting='hard')

        scores = cross_val_score(voting, faces, labels, cv=args.cv, n_jobs=-1)

        os.makedirs(os.path.dirname(args.plot_file), exist_ok=True)
        plt.figure(figsize=(8, 4))
        plt.plot(range(1, len(scores) + 1), scores, marker='o', linestyle='-')
        plt.title(f'Cross-validated accuracy ({args.cv}-fold)')
        plt.xlabel('Fold')
        plt.ylabel('Accuracy')
        plt.ylim(0, 1.0)
        plt.grid(True, linestyle='--', alpha=0.4)
        plt.tight_layout()
        plt.savefig(args.plot_file)
        print(f'Saved accuracy plot to: {args.plot_file}')

    if args.learning_curve:
        # Generate a learning curve (train vs validation accuracy for increasing training set size)
        knn = KNeighborsClassifier(n_neighbors=5)
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        voting = VotingClassifier(estimators=[('knn', knn), ('rf', rf)], voting='hard')

        plot_learning_curve(voting, faces, labels, cv=args.cv, output_file=args.curve_file)
        print(f'Saved learning curve plot to: {args.curve_file}')


if __name__ == '__main__':
    main()
