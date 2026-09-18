from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score

y_true = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
y_pred = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

print(f"Matriz: {confusion_matrix(y_true, y_pred).tolist()}")
print(f"Acurácia: {accuracy_score(y_true, y_pred):.2f} | "
      f"Precisão: {precision_score(y_true, y_pred):.2f} | "
      f"Recall: {recall_score(y_true, y_pred):.2f} | "
      f"F1: {f1_score(y_true, y_pred):.2f}")

# Por que a acurácia sozinha engana:
# Com 80% de tráfego normal, um modelo que diz "normal" para tudo já tem 0.80 de acurácia sem detectar nada.
# Aqui a acurácia 0.90 parece ótima, mas o recall 0.50 mostra que METADE dos ataques passou despercebida.
